"""
TodoMovil Agente CRM — Motor de Certeza
Evalúa el nivel de certeza de los resultados RAG según tipo_fuente y completitud.
"""

from typing import List, Dict
from core.config import settings


class CertaintyEngine:
    """
    Motor de evaluación de certeza.

    Niveles:
    - Alta: tipo_fuente = oficial_fabricante o verificacion_manual, datos completos
    - Media: tipo_fuente = web_search o datos parcialmente completos
    - Baja: sin datos, datos contradictorios, o solo LLM

    Factores que bajan certeza:
    - Falta de campo variante (arquitectura eléctrica desconocida)
    - tipo_fuente = feedback_vendedor (no verificado)
    - Conflicto entre fuentes
    """

    # Pesos por tipo de fuente
    FUENTE_WEIGHTS = {
        "oficial_fabricante": 1.0,
        "verificacion_manual": 0.9,
        "web_search": 0.5,
        "feedback_vendedor": 0.3,
    }

    # Campos requeridos para certeza Alta
    REQUIRED_FIELDS_ALTA = [
        "producto_id",
        "marca_vehiculo",
        "modelo_vehiculo",
        "sistema",
        "semaforo",
    ]

    def evaluate(self, results: List[Dict]) -> str:
        """
        Evaluar certeza global de los resultados RAG.
        Devuelve: "Alta" | "Media" | "Baja"
        """
        if not results:
            return "Baja"

        # Calcular score promedio
        scores = []
        for result in results:
            meta = result.get("metadata", {})
            score = self._score_single(meta)
            scores.append(score)

        avg_score = sum(scores) / len(scores)

        # Clasificar según thresholds
        if avg_score >= settings.RAG_CERTAINTY_HIGH:
            return "Alta"
        elif avg_score >= settings.RAG_CERTAINTY_MEDIUM:
            return "Media"
        else:
            return "Baja"

    def _score_single(self, metadata: Dict) -> float:
        """Calcular score de certeza para un solo resultado."""
        score = 0.0

        # Peso por tipo de fuente
        tipo_fuente = metadata.get("tipo_fuente", "feedback_vendedor")
        score += self.FUENTE_WEIGHTS.get(tipo_fuente, 0.3) * 0.4

        # Completitud de campos
        filled_fields = sum(
            1 for field in self.REQUIRED_FIELDS_ALTA
            if metadata.get(field)
        )
        completeness = filled_fields / len(self.REQUIRED_FIELDS_ALTA)
        score += completeness * 0.35

        # Presencia de variante (arquitectura eléctrica)
        has_variante = bool(metadata.get("variante"))
        score += (0.25 if has_variante else 0.05)

        # Semáforo influye
        semaforo = metadata.get("semaforo", "")
        if semaforo == "verde":
            score += 0.1
        elif semaforo == "amarillo":
            score -= 0.05
        elif semaforo == "rojo":
            score -= 0.1

        return min(max(score, 0.0), 1.0)  # Clamp entre 0 y 1
