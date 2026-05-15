"""
TodoMovil Agente CRM — Motor de Embeddings (DEPRECADO)

NOTA: Las embeddings ahora son manejadas por el servidor ChromaDB.
Este modulo se mantiene solo como referencia. No se usa en produccion.
El servidor ChromaDB usa all-MiniLM-L6-v2 por defecto.
"""


class EmbeddingEngine:
    """
    Motor de embeddings — DEPRECADO.
    Las embeddings son computadas por el servidor ChromaDB automaticamente.
    Este stub existe para compatibilidad con imports existentes.
    """

    def __init__(self):
        self._model = None

    def encode(self, text: str) -> list:
        """DEPRECADO — ChromaDB server maneja embeddings."""
        raise NotImplementedError(
            "Las embeddings son manejadas por el servidor ChromaDB. "
            "Use ChromaClient.query() con query_texts en vez de embeddings."
        )

    def encode_batch(self, texts: list) -> list:
        """DEPRECADO — ChromaDB server maneja embeddings."""
        raise NotImplementedError(
            "Las embeddings son manejadas por el servidor ChromaDB. "
            "Use ChromaClient.add_chunks() con documents en vez de embeddings."
        )

    def similarity(self, embedding_a: list, embedding_b: list) -> float:
        """Calcular similitud coseno entre dos embeddings."""
        dot = sum(a * b for a, b in zip(embedding_a, embedding_b))
        norm_a = sum(a * a for a in embedding_a) ** 0.5
        norm_b = sum(b * b for b in embedding_b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
