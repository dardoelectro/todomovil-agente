"""
TodoMovil Agente CRM — Web Search Engine (Capa 2)
Búsqueda web controlada con citación de URLs.
Certeza máxima: Media (nunca Alta sin verificación).
"""

from typing import List, Dict, Optional
from core.config import settings


class WebSearchEngine:
    """
    Motor de búsqueda web para la capa 2 del RAG.

    Características:
    - Siempre cita la URL fuente
    - Certeza máxima = Media (nunca Alta)
    - Solo se activa si Capa 1 devuelve certeza Baja
    - Resultados se marcan como tipo_fuente = web_search
    """

    def __init__(self):
        self._client = None

    async def _get_client(self):
        """Inicializar cliente z-ai-web-dev-sdk."""
        if self._client is None:
            try:
                import ZAI from 'z-ai-web-dev-sdk'
                self._client = await ZAI.create()
            except ImportError:
                self._client = None
        return self._client

    async def search(self, query: str, num_results: Optional[int] = None) -> List[Dict]:
        """
        Buscar en web y devolver resultados con URLs.

        Args:
            query: Consulta de búsqueda
            num_results: Número máximo de resultados

        Returns:
            Lista de dicts con: url, name, snippet, host_name, rank, date
        """
        max_results = num_results or settings.WEB_SEARCH_MAX_RESULTS

        # Enriquecer query con contexto TodoMovil
        enriched_query = f"diagnóstico automotor scanner {query}"

        try:
            client = await self._get_client()
            if client:
                results = await client.functions.invoke(
                    "web_search",
                    query=enriched_query,
                    num=max_results,
                )
                return self._process_results(results)
            else:
                return await self._search_fallback(enriched_query, max_results)
        except Exception as e:
            return []

    def _process_results(self, results: List) -> List[Dict]:
        """Procesar y normalizar resultados de web search."""
        processed = []
        for item in results:
            processed.append({
                "url": item.get("url", ""),
                "name": item.get("name", ""),
                "snippet": item.get("snippet", ""),
                "host_name": item.get("host_name", ""),
                "rank": item.get("rank", 0),
                "date": item.get("date", ""),
                "tipo_fuente": "web_search",
                "certezza": "Media",
            })
        return processed

    async def _search_fallback(self, query: str, num_results: int) -> List[Dict]:
        """Fallback si z-ai-web-dev-sdk no está disponible."""
        # TODO: Implementar con httpx si es necesario
        return []
