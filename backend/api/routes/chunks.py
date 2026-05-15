"""
TodoMovil Agente CRM — Ruta de Chunks
Gestión de sub-chunks vectorizados para RAG.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

router = APIRouter()


# ── Enums ─────────────────────────────────────────────────

class ChunkCategory(str, Enum):
    scanner = "scanner"
    medicion = "medicion"
    perfil_cliente = "perfil_cliente"
    objeciones = "objeciones"


# ── Modelos ───────────────────────────────────────────────

class ChunkMetadata(BaseModel):
    producto_id: str
    categoria: ChunkCategory
    marca_vehiculo: Optional[str] = None
    modelo_vehiculo: Optional[str] = None
    anio_inicio: Optional[int] = None
    anio_fin: Optional[int] = None
    sistema: Optional[str] = None
    variante: Optional[str] = None
    tipo_fuente: str = "oficial_fabricante"
    certezza: str = "Alta"  # Alta | Media | Baja
    semaforo: Optional[str] = None  # verde | amarillo | rojo | no_aplica


class ChunkCreate(BaseModel):
    content: str
    metadata: ChunkMetadata


class ChunkResponse(BaseModel):
    id: str
    content: str
    metadata: ChunkMetadata
    similarity: Optional[float] = None


class ChunkSearchRequest(BaseModel):
    query: str
    categoria: Optional[ChunkCategory] = None
    top_k: int = 5
    similarity_threshold: float = 0.65


# ── Endpoints ─────────────────────────────────────────────

@router.post("/", status_code=201)
async def create_chunk(chunk: ChunkCreate):
    """
    Crear un nuevo sub-chunk en ChromaDB.
    Cada chunk representa un dato atómico (1 producto × 1 sistema × 1 vehículo).
    """
    # TODO: Implementar inserción real en ChromaDB
    return {
        "status": "created",
        "content_preview": chunk.content[:100] + "..." if len(chunk.content) > 100 else chunk.content,
        "metadata": chunk.metadata.dict(),
    }


@router.post("/batch", status_code=201)
async def create_chunks_batch(chunks: List[ChunkCreate]):
    """Crear múltiples chunks de una vez (carga masiva)."""
    # TODO: Implementar inserción batch en ChromaDB
    return {
        "status": "created",
        "count": len(chunks),
    }


@router.post("/search", response_model=List[ChunkResponse])
async def search_chunks(request: ChunkSearchRequest):
    """
    Buscar chunks por similitud semántica.
    Este es el corazón de la capa 1 del RAG.
    """
    # TODO: Implementar búsqueda real en ChromaDB
    return [
        {
            "id": "demo_001",
            "content": f"Resultado demo para: '{request.query}'",
            "metadata": {
                "producto_id": "crp239",
                "categoria": "scanner",
                "marca_vehiculo": "Peugeot",
                "modelo_vehiculo": "208",
                "sistema": "Motor",
                "tipo_fuente": "oficial_fabricante",
                "certezza": "Alta",
                "semaforo": "verde",
            },
            "similarity": 0.92,
        }
    ]


@router.get("/stats")
async def chunks_stats():
    """Estadísticas de chunks cargados."""
    # TODO: Implementar conteo real desde ChromaDB
    return {
        "total_chunks": 0,
        "by_category": {
            "scanner": 0,
            "medicion": 0,
            "perfil_cliente": 0,
            "objeciones": 0,
        },
        "by_certezza": {
            "Alta": 0,
            "Media": 0,
            "Baja": 0,
        },
        "by_fuente": {
            "oficial_fabricante": 0,
            "verificacion_manual": 0,
            "web_search": 0,
            "feedback_vendedor": 0,
        },
    }
