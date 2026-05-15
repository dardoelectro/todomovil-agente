"""
TodoMovil Agente CRM — Tests del motor RAG
"""

import pytest
from core.certainty import CertaintyEngine
from core.rag_engine import RAGEngine


class TestCertaintyEngine:
    """Tests del motor de certeza."""

    def setup_method(self):
        self.engine = CertaintyEngine()

    def test_empty_results_returns_baja(self):
        """Sin resultados → certeza Baja."""
        result = self.engine.evaluate([])
        assert result == "Baja"

    def test_oficial_fabricante_with_all_fields_returns_alta(self):
        """Fuente oficial con todos los campos → certeza Alta."""
        results = [{
            "content": "CRP239 cubre Motor en Peugeot 208",
            "metadata": {
                "producto_id": "crp239",
                "marca_vehiculo": "Peugeot",
                "modelo_vehiculo": "208",
                "sistema": "Motor",
                "semaforo": "verde",
                "tipo_fuente": "oficial_fabricante",
                "variante": "V1 ECU Bosch",
            },
        }]
        result = self.engine.evaluate(results)
        assert result == "Alta"

    def test_web_search_returns_media_max(self):
        """Fuente web search → certeza Media como máximo."""
        results = [{
            "content": "Dato de web",
            "metadata": {
                "producto_id": "crp239",
                "marca_vehiculo": "Peugeot",
                "modelo_vehiculo": "208",
                "sistema": "Motor",
                "semaforo": "verde",
                "tipo_fuente": "web_search",
            },
        }]
        result = self.engine.evaluate(results)
        assert result in ["Media", "Baja"]  # Nunca Alta

    def test_feedback_vendedor_returns_media_or_baja(self):
        """Fuente feedback_vendedor → certeza Media o Baja."""
        results = [{
            "content": "Dato de vendedor",
            "metadata": {
                "producto_id": "crp239",
                "marca_vehiculo": "Peugeot",
                "modelo_vehiculo": "208",
                "sistema": "Motor",
                "semaforo": "verde",
                "tipo_fuente": "feedback_vendedor",
            },
        }]
        result = self.engine.evaluate(results)
        assert result in ["Media", "Baja"]  # Nunca Alta


class TestRAGEngineSemaforo:
    """Tests del cálculo de semáforo."""

    def setup_method(self):
        self.engine = RAGEngine()

    def test_immo_question_returns_amarillo(self):
        """Pregunta sobre IMMO → siempre AMARILLO."""
        result = self.engine._calculate_semaforo([], "¿Este scanner hace IMMO?")
        assert result["color"] == "amarillo"

    def test_inmovilizador_question_returns_amarillo(self):
        """Pregunta sobre inmovilizador → AMARILLO."""
        result = self.engine._calculate_semaforo([], "¿Cubre el inmovilizador?")
        assert result["color"] == "amarillo"

    def test_rojo_in_results_returns_rojo(self):
        """Resultado ROJO en datos → semáforo ROJO."""
        results = [{
            "metadata": {"semaforo": "rojo"},
        }]
        result = self.engine._calculate_semaforo(results, "¿Funciona con este auto?")
        assert result["color"] == "rojo"

    def test_no_aplica_returns_no_aplica(self):
        """Resultado no_aplica → semáforo no_aplica."""
        results = [{
            "metadata": {"semaforo": "no_aplica"},
        }]
        result = self.engine._calculate_semaforo(results, "¿Cubre BSI?")
        assert result["color"] == "no_aplica"

    def test_verde_all_clear(self):
        """Todos datos verdes → semáforo VERDE."""
        results = [{
            "metadata": {"semaforo": "verde"},
        }]
        result = self.engine._calculate_semaforo(results, "¿Lee códigos de Motor?")
        assert result["color"] == "verde"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
