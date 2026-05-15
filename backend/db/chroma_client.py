"""
TodoMovil Agente CRM — Cliente ChromaDB
Conexión y operaciones con la base de datos vectorial.
"""

from typing import List, Dict, Optional
from core.config import settings


class ChromaClient:
    """
    Cliente para ChromaDB — Base de datos vectorial.

    Colecciones:
    - scanners: Sub-chunks de escáneres (producto × sistema × vehículo)
    - medicion: Sub-chunks de herramientas de medición
    - perfil_cliente: Perfiles de clientes tipo
    - objeciones: Respuestas a objeciones comunes
    """

    def __init__(self):
        self._client = None

    async def connect(self):
        """Conectar a ChromaDB."""
        import chromadb
        self._client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
        )

    async def get_or_create_collection(self, name: str):
        """Obtener o crear una colección."""
        if self._client is None:
            await self.connect()
        return self._client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )

    async def add_chunks(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: List[Dict],
        ids: List[str],
    ):
        """Agregar chunks a una colección."""
        collection = await self.get_or_create_collection(collection_name)
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )

    async def query(
        self,
        collection_name: str,
        query_texts: List[str],
        n_results: int = 5,
        where: Optional[Dict] = None,
    ) -> Dict:
        """
        Buscar chunks por similitud semántica.

        Args:
            collection_name: Nombre de la colección
            query_texts: Textos de consulta
            n_results: Número de resultados
            where: Filtros de metadata

        Returns:
            Resultados de ChromaDB con documents, metadatas, distances, ids
        """
        collection = await self.get_or_create_collection(collection_name)
        return collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

    async def get_stats(self) -> Dict:
        """Obtener estadísticas de todas las colecciones."""
        if self._client is None:
            await self.connect()

        stats = {}
        for name in ["scanners", "medicion", "perfil_cliente", "objeciones"]:
            try:
                collection = self._client.get_collection(name)
                stats[name] = {"count": collection.count()}
            except Exception:
                stats[name] = {"count": 0}

        return stats
