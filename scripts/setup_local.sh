#!/bin/bash
# ══════════════════════════════════════════════════════════
# TodoMovil Agente — Setup local (desarrollo sin Docker)
# ══════════════════════════════════════════════════════════

set -e

echo "============================================================"
echo "TodoMovil Agente — Setup Local"
echo "============================================================"

# ── Verificar dependencias ────────────────────────────────
echo ""
echo "🔍 Verificando dependencias..."

command -v python3 &>/dev/null || { echo "❌ Python 3 no encontrado"; exit 1; }
command -v node &>/dev/null || { echo "❌ Node.js no encontrado"; exit 1; }
command -v npm &>/dev/null || { echo "❌ npm no encontrado"; exit 1; }

echo "✅ Python: $(python3 --version)"
echo "✅ Node: $(node --version)"
echo "✅ npm: $(npm --version)"

# ── Backend ────────────────────────────────────────────────
echo ""
echo "📦 Configurando backend..."

cd backend

# Crear venv si no existe
if [ ! -d "venv" ]; then
    echo "  Creando virtual environment..."
    python3 -m venv venv
fi

# Activar venv
source venv/bin/activate

# Instalar dependencias
echo "  Instalando dependencias Python..."
pip install -r requirements.txt --quiet

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo "  Creando .env desde .env.example..."
    cp ../.env.example ../.env
    echo "  ⚠️  Editar ../.env con tus valores reales"
fi

cd ..

# ── Frontend ───────────────────────────────────────────────
echo ""
echo "📦 Configurando frontend..."

cd frontend

# Instalar dependencias
echo "  Instalando dependencias Node.js..."
npm install --silent

cd ..

# ── Listo ──────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "✅ Setup completo!"
echo ""
echo "Para iniciar el desarrollo:"
echo ""
echo "  # Terminal 1 — Backend:"
echo "  cd backend && source venv/bin/activate"
echo "  uvicorn api.main:app --reload --port 8000"
echo ""
echo "  # Terminal 2 — Frontend:"
echo "  cd frontend && npm run dev"
echo ""
echo "  # O con Docker:"
echo "  docker-compose up --build"
echo ""
echo "============================================================"
