"""
TodoMovil Agente CRM — Web Search Engine (Capa 2)
Búsqueda web controlada con citación de URLs.
Certeza máxima: Media (nunca Alta sin verificación).
Usa la API de búsqueda via httpx.
"""

from typing import List, Dict, Optional
from core.config import settings
import httpx
import os


class WebSearchEngine:
    def __init__(self):
        self._api_key = os.getenv("ZAI_API_KEY", settings.ZAI_API_KEY)
        self._base_url = "https://open.bigmodel.cn/api/paas/v4/functions/invoke"

    async def search(self, query: str, num_results: Optional[int] = None) -> List[Dict]:
        max_results = num_results or settings.WEB_SEARCH_MAX_RESULTS
        enriched_query = f"diagnostico automotor scanner {query}"

        if not self._api_key or self._api_key == "your_zai_api_key_here":
            return []

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    self._base_url,
                    headers={"Authorization": f"Bearer {self._api_key}"},
                    json={
                        "function": "web_search",
                        "parameters": {
                            "query": enriched_query,
                            "num": max_results,
                        },
                    },
                )
                response.raise_for_status()
                data = response.json()
                results = data.get("results", data.get("data", []))
                return self._process_results(results)
        except Exception:
            return []

    def _process_results(self, results: List) -> List[Dict]:
        processed = []
        for item in results:
            processed.append({
                "url": item.get("url", ""),
                "name": item.get("name", ""),
                "snippet": item.get("snippet", ""),
                "host_name": item.get("host_name", ""),
                "rank": item.get("rank", 0),
                "date": item.get("date", ""),
                "tipo_fuente": "web_search",
                "certezza": "Media",
            })
        return processed
