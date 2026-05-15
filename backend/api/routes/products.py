"""
TodoMovil Agente CRM — Ruta de Productos
CRUD y búsqueda de productos (escáneres, multímetros, osciloscopios, etc.)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

router = APIRouter()


# ── Enums ─────────────────────────────────────────────────

class TipoHerramienta(str, Enum):
    scanner = "scanner"
    medicion = "medicion"
    programacion = "programacion"
    accesorio = "accesorio"


class SemaforoColor(str, Enum):
    verde = "verde"
    amarillo = "amarillo"
    rojo = "rojo"
    no_aplica = "no_aplica"


class NivelCertezza(str, Enum):
    alta = "Alta"
    media = "Media"
    baja = "Baja"


# ── Modelos ───────────────────────────────────────────────

class Producto(BaseModel):
    id: str
    nombre: str
    marca: str
    tipo: TipoHerramienta
    precio_lista: Optional[float] = None
    gamma: str  # entrada | media | alta
    sistemas_cobertura: List[str] = []
    funciones_especiales: List[str] = []
    semaforo_default: SemaforoColor = SemaforoColor.verde
    notas: Optional[str] = None


class ProductoCompatibilidad(BaseModel):
    producto_id: str
    marca_vehiculo: str
    modelo_vehiculo: str
    anio_inicio: int
    anio_fin: int
    motor: Optional[str] = None
    variante: Optional[str] = None
    sistema: str
    nivel_acceso: str  # lee_codigos | interactua | funciones_especiales
    semaforo: SemaforoColor
    certezza: NivelCertezza
    tipo_fuente: str
    notas: Optional[str] = None


# ── Datos demo (luego desde PostgreSQL) ───────────────────

PRODUCTOS_DEMO = [
    {
        "id": "crp239",
        "nombre": "CRP239",
        "marca": "Launch",
        "tipo": "scanner",
        "precio_lista": 450000,
        "gamma": "entrada",
        "sistemas_cobertura": ["Motor", "Transmisión", "ABS", "SRS"],
        "funciones_especiales": ["Reset aceite", "Reset frenos", "Bateria register"],
        "semaforo_default": "verde",
        "notas": "Gama entrada. No cubre BSI/Abs windows. IMMO = AMARILLO.",
    },
    {
        "id": "topscan_pro",
        "nombre": "TopScan Pro",
        "marca": "TopDon",
        "tipo": "scanner",
        "precio_lista": 350000,
        "gamma": "entrada",
        "sistemas_cobertura": ["Motor", "ABS", "SRS", "Transmisión"],
        "funciones_especiales": ["Reset aceite", "EPB reset"],
        "semaforo_default": "verde",
        "notas": "Gama entrada económica. Funciones especiales limitadas.",
    },
    {
        "id": "mx900",
        "nombre": "MaxiDiag MX900",
        "marca": "Autel",
        "tipo": "scanner",
        "precio_lista": 650000,
        "gamma": "media",
        "sistemas_cobertura": ["Motor", "Transmisión", "ABS", "SRS", "Direccion", "Carroceria", "Chasis"],
        "funciones_especiales": ["Reset aceite", "EPB", "SAS", "DPF", "IMMO", "BMS", "TPMS"],
        "semaforo_default": "verde",
        "notas": "Gama media. IMMO = AMARILLO (no confiable en todas las marcas). Cubre más sistemas que CRP239.",
    },
    {
        "id": "ds900",
        "nombre": "MaxiDAS DS900",
        "marca": "Autel",
        "tipo": "scanner",
        "precio_lista": 1200000,
        "gamma": "alta",
        "sistemas_cobertura": ["Motor", "Transmisión", "ABS", "SRS", "Direccion", "Carroceria", "Chasis", "Confort", "BSI", "Infotainment"],
        "funciones_especiales": ["Bi-direccional", "Coding", "Adaptaciones", "IMMO", "EPB", "SAS", "DPF", "BMS", "TPMS", "Injector coding"],
        "semaforo_default": "verde",
        "notas": "Gama alta. Bi-direccional. IMMO = AMARILLO. BSI coverage amplio.",
    },
]


# ── Endpoints ─────────────────────────────────────────────

@router.get("/", response_model=List[Producto])
async def list_products(
    tipo: Optional[TipoHerramienta] = Query(None, description="Filtrar por tipo de herramienta"),
    gamma: Optional[str] = Query(None, description="Filtrar por gamma"),
):
    """Listar todos los productos con filtros opcionales."""
    results = PRODUCTOS_DEMO
    if tipo:
        results = [p for p in results if p["tipo"] == tipo.value]
    if gamma:
        results = [p for p in results if p["gamma"] == gamma.value]
    return results


@router.get("/{producto_id}", response_model=Producto)
async def get_product(producto_id: str):
    """Obtener detalle de un producto por ID."""
    for p in PRODUCTOS_DEMO:
        if p["id"] == producto_id:
            return p
    raise HTTPException(status_code=404, detail=f"Producto '{producto_id}' no encontrado")


@router.get("/{producto_id}/compatibilidad")
async def get_compatibilidad(
    producto_id: str,
    marca: Optional[str] = Query(None),
    modelo: Optional[str] = Query(None),
):
    """Obtener datos de compatibilidad de un producto."""
    # Demo — luego consultar chunks vectorizados + PostgreSQL
    return {
        "producto_id": producto_id,
        "marca": marca,
        "modelo": modelo,
        "resultados": "Funcionalidad disponible tras cargar chunks de datos.",
    }
