"""
TodoMovil Agente CRM — Ruta del Chat (núcleo RAG)
Pipeline de 3 capas: Base curada → Web Search → LLM (solo forma).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from core.rag_engine import RAGEngine
from core.config import settings

router = APIRouter()

# Instancia global del motor RAG (se inicializa al arrancar)
rag_engine: Optional[RAGEngine] = None


def get_rag_engine() -> RAGEngine:
    global rag_engine
    if rag_engine is None:
        rag_engine = RAGEngine()
    return rag_engine


# ── Modelos ───────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_history: List[ChatMessage] = []
    vendedor: Optional[str] = None
    contexto_cliente: Optional[dict] = None


class SourceReference(BaseModel):
    tipo_fuente: str  # oficial_fabricante | verificacion_manual | web_search | feedback_vendedor
    producto: str
    sistema: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    url: Optional[str] = None
    certezza: str  # Alta | Media | Baja


class SemaforoResult(BaseModel):
    color: str  # verde | amarillo | rojo | no_aplica
    motivo: str
    detalle: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    fuentes: List[SourceReference] = []
    semaforo: Optional[SemaforoResult] = None
    certeza_global: str  # Alta | Media | Baja
    capa_utilizada: str  # base_curada | web_search | llm_forma
    productos_mencionados: List[str] = []


# ── Endpoints ─────────────────────────────────────────────

@router.post("/ask", response_model=ChatResponse)
async def ask_agent(request: ChatRequest):
    """
    Endpoint principal del copiloto.
    Recibe pregunta del vendedor y devuelve respuesta con semáforo + certeza.
    """
    engine = get_rag_engine()

    try:
        result = await engine.query(
            question=request.message,
            history=request.conversation_history,
            vendedor=request.vendedor,
            contexto_cliente=request.contexto_cliente,
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en RAG: {str(e)}")


@router.post("/ask/simple")
async def ask_simple(message: str):
    """Endpoint simplificado para pruebas rápidas."""
    engine = get_rag_engine()
    result = await engine.query(question=message)
    return {"reply": result.get("reply", ""), "semaforo": result.get("semaforo")}
