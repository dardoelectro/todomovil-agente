"""
TodoMovil Agente CRM — Motor RAG (Retrieval-Augmented Generation)
Pipeline de 3 capas:
  Capa 1: Base curada (ChromaDB) — certeza Alta/Media
  Capa 2: Web Search controlado con URLs — certeza Media/Baja
  Capa 3: LLM solo para FORMA (redaccion), NUNCA para contenido
"""

from typing import List, Optional, Dict, Any
from core.config import settings
from core.certainty import CertaintyEngine
from core.web_search import WebSearchEngine
from core.llm_client import LLMClient
from db.chroma_client import ChromaClient


class RAGEngine:
    """
    Motor RAG del copiloto del vendedor.

    Flujo:
    1. Recibir pregunta del vendedor
    2. Buscar en base curada (ChromaDB) — Capa 1
    3. Si certeza < threshold, buscar en web — Capa 2
    4. Redactar respuesta con LLM (solo forma, datos de capas 1-2) — Capa 3
    5. Aplicar semaforo + certeza
    6. Devolver respuesta con fuentes
    """

    def __init__(self):
        self.chroma = ChromaClient()
        self.certainty_engine = CertaintyEngine()
        self.web_search = WebSearchEngine()
        self.llm_client = LLMClient()

    async def query(
        self,
        question: str,
        history: Optional[List[Dict]] = None,
        vendedor: Optional[str] = None,
        contexto_cliente: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Procesar una consulta del vendedor a traves del pipeline RAG."""
        # Paso 1: Buscar en base curada
        curated_results = await self._search_curated(question)
        # Paso 2: Evaluar certeza
        certainty_level = self.certainty_engine.evaluate(curated_results)
        web_results = []
        capa_utilizada = "base_curada"
        # Paso 3: Si certeza baja, buscar en web
        if certainty_level == "Baja" and settings.WEB_SEARCH_ENABLED:
            web_results = await self.web_search.search(question)
            if web_results:
                capa_utilizada = "web_search"
                certainty_level = "Media"
        # Paso 4: Redactar respuesta con LLM
        reply = await self._generate_reply(
            question=question,
            curated_data=curated_results,
            web_data=web_results,
            history=history,
        )
        # Paso 5: Calcular semaforo
        semaforo = self._calculate_semaforo(curated_results=curated_results, question=question)
        # Paso 6: Consolidar fuentes
        fuentes = self._consolidate_sources(curated_results, web_results)
        # Paso 7: Extraer productos
        productos = self._extract_products(curated_results)

        return {
            "reply": reply,
            "fuentes": fuentes,
            "semaforo": semaforo,
            "certeza_global": certainty_level,
            "capa_utilizada": capa_utilizada,
            "productos_mencionados": productos,
        }

    async def _search_curated(self, question: str) -> List[Dict]:
        """
        Capa 1: Busqueda en base curada (ChromaDB).
        Busca en todas las colecciones y consolida resultados.
        ChromaDB server genera las embeddings automaticamente.
        """
        all_results = []
        for collection_name in ["scanners", "medicion", "perfil_cliente", "objeciones"]:
            try:
                results = await self.chroma.query(
                    collection_name=collection_name,
                    query_texts=[question],
                    n_results=settings.RAG_TOP_K,
                )
                if results and results.get("documents"):
                    docs = results["documents"][0] if results["documents"] else []
                    metas = results["metadatas"][0] if results["metadatas"] else []
                    dists = results["distances"][0] if results["distances"] else []
                    for doc, meta, dist in zip(docs, metas, dists):
                        similarity = 1 - dist
                        if similarity >= settings.RAG_SIMILARITY_THRESHOLD:
                            all_results.append({
                                "content": doc,
                                "metadata": meta or {},
                                "score": similarity,
                            })
            except Exception:
                continue
        all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return all_results[:settings.RAG_TOP_K]

    async def _generate_reply(self, question, curated_data, web_data, history=None):
        """Capa 3: Generar respuesta usando LLM. Solo redacta, NUNCA inventa."""
        context = self._build_context(curated_data, web_data)
        system_prompt = (
            "Eres el copiloto del vendedor de TodoMovil, una casa de repuestos "
            "y herramientas de diagnostico automotor con 40 anos en Argentina. "
            "Tu trabajo es asistir al vendedor con informacion precisa sobre "
            "compatibilidad de escaneres, multimetros, osciloscopios y otras "
            "herramientas de diagnostico.\n\n"
            "REGLAS ESTRICTAS:\n"
            "1. Solo usa la informacion proporcionada en el CONTEXTO. "
            "NUNCA inventes datos de compatibilidad, funciones o precios.\n"
            "2. Si no hay informacion suficiente, dilo claramente: "
            "'No tengo datos confirmados sobre esa consulta.'\n"
            "3. Siempre menciona el nivel de certeza (Alta/Media/Baja).\n"
            "4. Si el semaforo es AMARILLO, incluye la advertencia explicita.\n"
            "5. Si el semaforo es ROJO, NO recomiendes el producto para ese uso.\n"
            "6. Cita las fuentes cuando sea posible.\n"
            "7. Responde en espanol argentino, cercano pero profesional.\n"
        )
        user_prompt = f"CONTEXTO:\n{context}\n\nPREGUNTA DEL VENDEDOR: {question}"
        try:
            response = await self.llm_client.chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                history=history,
            )
            return response
        except Exception:
            if curated_data:
                return self._format_raw_data(curated_data)
            return "Error al generar respuesta. Por favor, consulta las fichas tecnicas."

    def _build_context(self, curated_data, web_data):
        """Construir bloque de contexto para el LLM con datos reales."""
        parts = []
        if curated_data:
            parts.append("=== DATOS DE BASE CURADA ===")
            for i, item in enumerate(curated_data, 1):
                parts.append(f"[{i}] {item.get('content', '')}")
                meta = item.get("metadata", {})
                parts.append(
                    f"    Fuente: {meta.get('tipo_fuente', 'N/A')} | "
                    f"Certeza: {meta.get('certezza', 'N/A')} | "
                    f"Semaforo: {meta.get('semaforo', 'N/A')}"
                )
        if web_data:
            parts.append("\n=== DATOS DE WEB SEARCH ===")
            for i, item in enumerate(web_data, 1):
                parts.append(f"[W{i}] {item.get('snippet', '')}")
                parts.append(f"    URL: {item.get('url', 'N/A')}")
        if not parts:
            parts.append("No se encontraron datos en la base curada ni en web search.")
        return "\n".join(parts)

    def _calculate_semaforo(self, curated_results, question):
        """Calcular semaforo segun reglas de negocio."""
        if not curated_results:
            return {
                "color": "amarillo",
                "motivo": "Sin datos en base curada",
                "detalle": "Consultar ficha tecnica o contacto con fabricante",
            }
        question_lower = question.lower()
        if "immo" in question_lower or "inmovilizador" in question_lower:
            return {
                "color": "amarillo",
                "motivo": "Funcion IMMO no es confiable en todas las marcas/modelos",
                "detalle": "Solo ofrecer con advertencia explicita al cliente. "
                           "No garantizar cobertura IMMO completa.",
            }
        semaforos = [r.get("metadata", {}).get("semaforo") for r in curated_results]
        if "rojo" in semaforos:
            return {"color": "rojo", "motivo": "Incompatibilidad confirmada",
                    "detalle": "No ofrecer este producto para este vehiculo/sistema."}
        if "amarillo" in semaforos:
            return {"color": "amarillo", "motivo": "Datos parciales o cobertura limitada",
                    "detalle": "Ofrecer con advertencia."}
        if "no_aplica" in semaforos:
            return {"color": "no_aplica", "motivo": "Fuera de cobertura de gama",
                    "detalle": "El equipo no cubre ese sistema. No es incompatibilidad, es fuera de alcance."}
        return {"color": "verde", "motivo": "Datos verificados y completos",
                "detalle": "Producto compatible confirmado."}

    def _consolidate_sources(self, curated_data, web_data):
        """Consolidar fuentes de ambas capas."""
        sources = []
        for item in curated_data:
            meta = item.get("metadata", {})
            sources.append({
                "tipo_fuente": meta.get("tipo_fuente", "oficial_fabricante"),
                "producto": meta.get("producto_id", ""),
                "sistema": meta.get("sistema"),
                "marca": meta.get("marca_vehiculo"),
                "modelo": meta.get("modelo_vehiculo"),
                "url": None,
                "certezza": meta.get("certezza", "Alta"),
            })
        for item in web_data:
            sources.append({
                "tipo_fuente": "web_search", "producto": "",
                "sistema": None, "marca": None, "modelo": None,
                "url": item.get("url"), "certezza": "Media",
            })
        return sources

    def _extract_products(self, curated_data):
        """Extraer IDs de productos mencionados."""
        products = set()
        for item in curated_data:
            meta = item.get("metadata", {})
            if meta.get("producto_id"):
                products.add(meta["producto_id"])
        return list(products)

    def _format_raw_data(self, curated_data):
        """Formatear datos crudos cuando LLM no esta disponible."""
        lines = []
        for item in curated_data:
            lines.append(f"- {item.get('content', 'Sin datos')}")
            meta = item.get("metadata", {})
            lines.append(f"  (Certeza: {meta.get('certezza', 'N/A')} | Semaforo: {meta.get('semaforo', 'N/A')})")
        return "\n".join(lines)
