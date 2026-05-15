"""
TodoMovil Agente CRM — Cliente PostgreSQL
Conexión y modelos con SQLAlchemy.
"""

from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

# ── Engine y Session ──────────────────────────────────────

engine = create_engine(settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ── Modelos ───────────────────────────────────────────────

class Producto(Base):
    """Productos: escáneres, multímetros, osciloscopios, accesorios."""
    __tablename__ = "productos"

    id = Column(String(50), primary_key=True)
    nombre = Column(String(200), nullable=False)
    marca = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)  # scanner | medicion | programacion | accesorio
    gamma = Column(String(50))  # entrada | media | alta
    precio_lista = Column(Float)
    sistemas_cobertura = Column(JSON)  # Lista de sistemas
    funciones_especiales = Column(JSON)
    semaforo_default = Column(String(20))
    notas = Column(Text)
    fecha_actualizacion = Column(DateTime)


class Compatibilidad(Base):
    """Compatibilidad producto × vehículo × sistema."""
    __tablename__ = "compatibilidades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(String(50), nullable=False)
    marca_vehiculo = Column(String(100), nullable=False)
    modelo_vehiculo = Column(String(100), nullable=False)
    anio_inicio = Column(Integer)
    anio_fin = Column(Integer)
    motor = Column(String(100))
    variante = Column(String(200))  # Arquitectura eléctrica
    sistema = Column(String(100), nullable=False)
    nivel_acceso = Column(String(50))  # lee_codigos | interactua | funciones_especiales
    semaforo = Column(String(20))  # verde | amarillo | rojo | no_aplica
    certezza = Column(String(20))  # Alta | Media | Baja
    tipo_fuente = Column(String(50))
    codigo_falla = Column(String(100))  # Link a herramienta de medición
    notas = Column(Text)
    chunk_id = Column(String(100))  # Referencia al chunk en ChromaDB


class Vendedor(Base):
    """Vendedores de TodoMovil."""
    __tablename__ = "vendedores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    password_hash = Column(String(500), nullable=False)
    rol = Column(String(50))  # vendedor | vendedor_avanzado | admin
    activo = Column(Integer, default=1)


class Conversacion(Base):
    """Historial de conversaciones del agente."""
    __tablename__ = "conversaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vendedor_id = Column(Integer)
    pregunta = Column(Text, nullable=False)
    respuesta = Column(Text)
    semaforo = Column(String(20))
    certezza = Column(String(20))
    capa_utilizada = Column(String(50))
    fuentes = Column(JSON)
    created_at = Column(DateTime)


# ── Funciones de utilidad ─────────────────────────────────

def get_db():
    """Dependency para obtener sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Crear todas las tablas."""
    Base.metadata.create_all(bind=engine)
