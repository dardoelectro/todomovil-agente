"""
TodoMovil Agente CRM — Backend FastAPI
Punto de entrada principal de la API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, products, chunks, auth
from core.config import settings

app = FastAPI(
    title="TodoMovil Agente CRM",
    description="API del copiloto del vendedor — RAG + Semáforo + Certeza",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Rutas ─────────────────────────────────────────────────
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(chunks.router, prefix="/api/chunks", tags=["chunks"])


@app.get("/", tags=["health"])
async def root():
    return {
        "service": "TodoMovil Agente CRM",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy"}
