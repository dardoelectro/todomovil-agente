"""
TodoMovil Agente CRM — Cliente LLM (z-ai-web-dev-sdk / GLM)
El LLM SOLO se usa para redactar respuestas (forma), NUNCA para generar contenido.
"""

from typing import List, Dict, Optional
from core.config import settings


class LLMClient:
    """
    Cliente para GLM via z-ai-web-dev-sdk.
    Se usa EXCLUSIVAMENTE para redactar la respuesta final
    con los datos obtenidos de las capas 1 y 2 del RAG.
    """

    def __init__(self):
        self._client = None

    async def _get_client(self):
        """Inicializar cliente z-ai-web-dev-sdk."""
        if self._client is None:
            try:
                import ZAI from 'z-ai-web-dev-sdk'
                self._client = await ZAI.create()
            except ImportError:
                # Fallback: usar API directa con httpx
                self._client = None
        return self._client

    async def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        history: Optional[List[Dict]] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Enviar consulta al LLM y devolver respuesta.

        Args:
            system_prompt: Instrucciones del sistema
            user_prompt: Pregunta del usuario con contexto RAG
            history: Historial de conversación previo
            temperature: Temperatura (default: settings.LLM_TEMPERATURE)

        Returns:
            Respuesta del LLM como string
        """
        temp = temperature or settings.LLM_TEMPERATURE

        # Construir mensajes
        messages = [{"role": "system", "content": system_prompt}]

        if history:
            for msg in history:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", ""),
                })

        messages.append({"role": "user", "content": user_prompt})

        try:
            client = await self._get_client()
            if client:
                # Usar z-ai-web-dev-sdk
                completion = await client.chat.completions.create(
                    messages=messages,
                    temperature=temp,
                    max_tokens=settings.LLM_MAX_TOKENS,
                )
                return completion.choices[0].message.content
            else:
                # Fallback con httpx
                return await self._chat_fallback(messages, temp)
        except Exception as e:
            return f"Error al consultar LLM: {str(e)}"

    async def _chat_fallback(self, messages: List[Dict], temperature: float) -> str:
        """Fallback usando httpx directo a la API de GLM."""
        import httpx
        import os

        api_key = os.getenv("ZAI_API_KEY", settings.ZAI_API_KEY)
        if not api_key:
            return "LLM no disponible. Consulta las fichas técnicas directamente."

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": settings.LLM_MODEL,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": settings.LLM_MAX_TOKENS,
                    },
                )
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error en fallback LLM: {str(e)}"
