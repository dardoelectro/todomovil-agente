"""
TodoMovil Agente CRM — Configuracion centralizada
Lee variables de entorno con valores por defecto.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # ── PostgreSQL ────────────────────────────────────────
    DATABASE_URL: str = "postgresql://tm_user:tm_secure_2025@localhost:5432/todomovil"

    # ── ChromaDB ──────────────────────────────────────────
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    # NOTA: Las embeddings las maneja el servidor ChromaDB automaticamente.
    # Modelo default del servidor: all-MiniLM-L6-v2 (via onnxruntime)

    # ── LLM ──────────────────────────────────────────────
    ZAI_API_KEY: str = ""
    LLM_MODEL: str = "glm-4"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 2048

    # ── FastAPI ───────────────────────────────────────────
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # ── Seguridad ─────────────────────────────────────────
    JWT_SECRET: str = "change_this_to_a_secure_random_string"
    JWT_EXPIRATION_HOURS: int = 24

    # ── RAG ──────────────────────────────────────────────
    RAG_TOP_K: int = 5
    RAG_SIMILARITY_THRESHOLD: float = 0.65
    RAG_CERTAINTY_HIGH: float = 0.85
    RAG_CERTAINTY_MEDIUM: float = 0.65

    # ── Web Search ────────────────────────────────────────
    WEB_SEARCH_ENABLED: bool = True
    WEB_SEARCH_MAX_RESULTS: int = 5

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
