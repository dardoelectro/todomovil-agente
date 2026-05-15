#!/usr/bin/env python3
"""
TodoMovil Agente — Script de carga de chunks a ChromaDB
Lee los archivos JSON de chunks y los inserta en la base vectorial.

Uso:
    python scripts/load_chunks.py [--category scanners|medicion|perfil_cliente|objeciones|all]
"""

import json
import asyncio
import sys
import os
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from db.chroma_client import ChromaClient


CHUNKS_DIR = Path(__file__).parent.parent / "backend" / "data" / "chunks"

CATEGORIES = {
    "scanners": "scanners",
    "medicion": "medicion",
    "perfil_cliente": "perfil_cliente",
    "objeciones": "objeciones",
}


async def load_category(category: str, client: ChromaClient):
    """Cargar todos los chunks de una categoría."""
    cat_dir = CHUNKS_DIR / category
    if not cat_dir.exists():
        print(f"  ⚠️  Directorio no encontrado: {cat_dir}")
        return 0

    json_files = list(cat_dir.glob("*.json"))
    total_loaded = 0

    for json_file in json_files:
        print(f"  📄 Cargando: {json_file.name}")
        with open(json_file, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        if not chunks:
            print(f"    ⚠️  Archivo vacío")
            continue

        documents = []
        metadatas = []
        ids = []

        for chunk in chunks:
            documents.append(chunk["content"])
            metadatas.append(chunk["metadata"])
            ids.append(chunk["id"])

        try:
            await client.add_chunks(
                collection_name=category,
                documents=documents,
                metadatas=metadatas,
                ids=ids,
            )
            total_loaded += len(chunks)
            print(f"    ✅ {len(chunks)} chunks cargados")
        except Exception as e:
            print(f"    ❌ Error: {e}")

    return total_loaded


async def main():
    category = sys.argv[2] if len(sys.argv) > 2 else "all"

    print("=" * 60)
    print("TodoMovil Agente — Cargador de Chunks")
    print("=" * 60)

    client = ChromaClient()
    await client.connect()

    total = 0

    if category == "all":
        for cat_name in CATEGORIES:
            print(f"\n📦 Categoría: {cat_name}")
            loaded = await load_category(cat_name, client)
            total += loaded
    else:
        if category not in CATEGORIES:
            print(f"❌ Categoría no válida: {category}")
            print(f"   Válidas: {', '.join(CATEGORIES.keys())}, all")
            sys.exit(1)
        print(f"\n📦 Categoría: {category}")
        loaded = await load_category(category, client)
        total += loaded

    print(f"\n{'=' * 60}")
    print(f"✅ Total chunks cargados: {total}")
    print(f"{'=' * 60}")

    # Mostrar estadísticas
    stats = await client.get_stats()
    print("\n📊 Estadísticas por colección:")
    for name, info in stats.items():
        print(f"  {name}: {info['count']} chunks")


if __name__ == "__main__":
    asyncio.run(main())
