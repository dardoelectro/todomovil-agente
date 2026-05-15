"""
TodoMovil Agente CRM — Cliente LLM (GLM via httpx)
El LLM SOLO se usa para redactar respuestas (forma), NUNCA para generar contenido.
"""

from typing import List, Dict, Optional
from core.config import settings
import httpx
import os


class LLMClient:
    """
    Cliente para GLM via API REST.
    Se usa EXCLUSIVAMENTE para redactar la respuesta final
    con los datos obtenidos de las capas 1 y 2 del RAG.
    """

    def __init__(self):
        self._api_key = os.getenv("ZAI_API_KEY", settings.ZAI_API_KEY)
        self._base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    async def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        history: Optional[List[Dict]] = None,
        temperature: Optional[float] = None,
    ) -> str:
        if not self._api_key or self._api_key == "your_zai_api_key_here":
            return "LLM no configurado. Verifica ZAI_API_KEY en .env."

        temp = temperature or settings.LLM_TEMPERATURE

        messages = [{"role": "system", "content": system_prompt}]

        if history:
            for msg in history:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", ""),
                })

        messages.append({"role": "user", "content": user_prompt})

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    self._base_url,
                    headers={"Authorization": f"Bearer {self._api_key}"},
                    json={
                        "model": settings.LLM_MODEL,
                        "messages": messages,
                        "temperature": temp,
                        "max_tokens": settings.LLM_MAX_TOKENS,
                    },
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            return f"Error HTTP del LLM: {e.response.status_code}"
        except httpx.TimeoutException:
            return "Timeout al consultar LLM. Intenta de nuevo."
        except Exception as e:
            return f"Error al consultar LLM: {str(e)}"
