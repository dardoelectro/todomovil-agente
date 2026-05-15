"""
TodoMovil Agente CRM — Ruta de autenticación
JWT simple para vendedores.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from core.config import settings

router = APIRouter()


# ── Modelos ───────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str = "vendedor"


class TokenData(BaseModel):
    username: Optional[str] = None


# ── Usuarios demo (luego migrar a PostgreSQL) ─────────────

DEMO_USERS = {
    "vendedor1": {"password": "tm2025", "role": "vendedor"},
    "admin": {"password": "tm_admin_2025", "role": "admin"},
    "ezequiel": {"password": "eze_tm2025", "role": "vendedor_avanzado"},
    "mauro": {"password": "mau_tm2025", "role": "vendedor_avanzado"},
}


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")


def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


# ── Endpoints ─────────────────────────────────────────────

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Autenticar vendedor y devolver JWT."""
    user = DEMO_USERS.get(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token(
        data={"sub": request.username, "role": user["role"]}
    )
    return LoginResponse(
        access_token=token,
        username=request.username,
        role=user["role"],
    )


@router.get("/me")
async def get_current_user(token: str = ""):
    """Devolver datos del usuario autenticado."""
    token_data = verify_token(token)
    user = DEMO_USERS.get(token_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"username": token_data.username, "role": user["role"]}
