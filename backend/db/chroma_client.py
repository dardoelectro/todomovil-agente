"""
TodoMovil Agente CRM — Cliente ChromaDB via REST API
Conexion y operaciones con la base de datos vectorial usando httpx.
El servidor ChromaDB maneja todas las embeddings automaticamente.
No requiere el paquete chromadb Python — mucho mas liviano.
"""

import httpx
from typing import List, Dict, Optional
from core.config import settings


class ChromaClient:
    """
    Cliente HTTP para ChromaDB — Base de datos vectorial.

    Usa la REST API de ChromaDB en vez del paquete Python,
    lo que elimina la necesidad de onnxruntime, torch, etc.
    El servidor ChromaDB maneja todas las embeddings.

    Colecciones:
    - scanners: Sub-chunks de escaneres (producto x sistema x vehiculo)
    - medicion: Sub-chunks de herramientas de medicion
    - perfil_cliente: Perfiles de clientes tipo
    - objeciones: Respuestas a objeciones comunes
    """

    def __init__(self):
        self._base_url = f"http://{settings.CHROMA_HOST}:{settings.CHROMA_PORT}/api/v1"
        self._client: Optional[httpx.Client] = None
        self._collections_cache: Dict[str, str] = {}

    def _get_client(self) -> httpx.Client:
        """Obtener o crear cliente HTTP."""
        if self._client is None:
            self._client = httpx.Client(timeout=30.0)
        return self._client

    async def connect(self):
        """Verificar conexion a ChromaDB."""
        client = self._get_client()
        try:
            response = client.get(f"{self._base_url}/heartbeat")
            response.raise_for_status()
            return True
        except Exception as e:
            raise ConnectionError(f"No se pudo conectar a ChromaDB: {e}")

    def _find_collection_id(self, name: str) -> Optional[str]:
        """Buscar UUID de coleccion por nombre."""
        if name in self._collections_cache:
            return self._collections_cache[name]
        client = self._get_client()
        try:
            response = client.get(f"{self._base_url}/collections")
            if response.status_code == 200:
                for coll in response.json():
                    if coll.get("name") == name:
                        self._collections_cache[name] = coll["id"]
                        return coll["id"]
        except Exception:
            pass
        return None

    async def get_or_create_collection(self, name: str, metadata: Optional[Dict] = None):
        """Obtener o crear una coleccion."""
        coll_id = self._find_collection_id(name)
        if coll_id:
            return coll_id
        client = self._get_client()
        body = {"name": name}
        if metadata:
            body["metadata"] = metadata
        response = client.post(f"{self._base_url}/collections", json=body)
        response.raise_for_status()
        result = response.json()
        self._collections_cache[name] = result["id"]
        return result["id"]

    async def add_chunks(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: List[Dict],
        ids: List[str],
    ):
        """Agregar chunks. El servidor ChromaDB genera las embeddings."""
        coll_id = await self.get_or_create_collection(
            collection_name, metadata={"hnsw:space": "cosine"}
        )
        client = self._get_client()
        body = {"ids": ids, "documents": documents, "metadatas": metadatas}
        response = client.post(
            f"{self._base_url}/collections/{coll_id}/add", json=body
        )
        response.raise_for_status()
        return response.json()

    async def query(
        self,
        collection_name: str,
        query_texts: List[str],
        n_results: int = 5,
        where: Optional[Dict] = None,
    ) -> Dict:
        """Buscar chunks por similitud semantica. El servidor genera embeddings."""
        coll_id = self._find_collection_id(collection_name)
        if not coll_id:
            coll_id = await self.get_or_create_collection(collection_name)
        client = self._get_client()
        body = {
            "query_texts": query_texts,
            "n_results": n_results,
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            body["where"] = where
        response = client.post(
            f"{self._base_url}/collections/{coll_id}/query", json=body
        )
        response.raise_for_status()
        return response.json()

    async def get_stats(self) -> Dict:
        """Obtener estadisticas de todas las colecciones."""
        client = self._get_client()
        stats = {}
        try:
            response = client.get(f"{self._base_url}/collections")
            if response.status_code == 200:
                for coll in response.json():
                    name = coll.get("name", "unknown")
                    coll_id = coll.get("id")
                    self._collections_cache[name] = coll_id
                    count = 0
                    try:
                        count_resp = client.get(
                            f"{self._base_url}/collections/{coll_id}/count"
                        )
                        if count_resp.status_code == 200:
                            count = count_resp.json()
                    except Exception:
                        pass
                    stats[name] = {"count": count}
        except Exception:
            pass
        for expected in ["scanners", "medicion", "perfil_cliente", "objeciones"]:
            if expected not in stats:
                stats[expected] = {"count": 0}
        return stats
