"""
TodoMovil Agente CRM — Motor de Embeddings
Genera embeddings con sentence-transformers para búsqueda semántica.
"""

from typing import List
from core.config import settings


class EmbeddingEngine:
    """
    Motor de embeddings usando sentence-transformers.
    Modelo: paraphrase-multilingual-MiniLM-L12-v2 (384 dimensiones)
    - Multilingüe (español incluido)
    - Liviano (120MB)
    - Rápido para inferencia
    """

    def __init__(self):
        self._model = None
        self._model_name = settings.EMBEDDING_MODEL

    @property
    def model(self):
        """Carga perezosa del modelo (lazy loading)."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self._model_name)
        return self._model

    def encode(self, text: str) -> List[float]:
        """Generar embedding para un texto."""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Generar embeddings para múltiples textos."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def similarity(self, embedding_a: List[float], embedding_b: List[float]) -> float:
        """Calcular similitud coseno entre dos embeddings."""
        import numpy as np
        a = np.array(embedding_a)
        b = np.array(embedding_b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
