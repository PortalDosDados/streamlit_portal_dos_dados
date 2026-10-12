"""
Testes unitários automatizados para as regras de negócio e cálculos do Portal dos Dados.
Utiliza a biblioteca padrão unittest para execução rápida e independente.
"""

from datetime import time
import unittest
import pandas as pd

from utils.business_rules import (
    parse_horario,
    classificar_severidade_parada,
    calcular_metricas_curva_s,
    validar_alocacao,
)


class TestBusinessRules(unittest.TestCase):

    def test_parse_horario_validos(self):
        # Formato HHMM
        t, s = parse_horario("1430")
        self.assertEqual(t, time(14, 30))
        self.assertEqual(s, "14:30")

        # Formato HMM
        t, s = parse_horario("830")
        self.assertEqual(t, time(8, 30))
        self.assertEqual(s, "08:30")

        # Formato HH
        t, s = parse_horario("14")
        self.assertEqual(t, time(14, 0))
        self.assertEqual(s, "14:00")

        # Formato HH:MM
        t, s = parse_horario("08:15")
        self.assertEqual(t, time(8, 15))
        self.assertEqual(s, "08:15")

    def test_parse_horario_invalidos(self):
        t, _ = parse_horario("2500")
        self.assertIsNone(t)

        t, _ = parse_horario("1265")
        self.assertIsNone(t)

        t, _ = parse_horario("")
        self.assertIsNone(t)

        t, _ = parse_horario(None)
        self.assertIsNone(t)

    def test_classificar_severidade_parada(self):
        status, cor = classificar_severidade_parada(0.5)
        self.assertIn("RELATÓRIO DE TURNO", status)
        self.assertEqual(cor, "#66bb6a")

        status, cor = classificar_severidade_parada(1.2)
        self.assertIn("FCA", status)
        self.assertEqual(cor, "#ffa726")

        status, cor = classificar_severidade_parada(2.5)
        self.assertIn("CRÍTICA", status)
        self.assertEqual(cor, "#ef5350")

    def test_calcular_metricas_curva_s_no_prazo(self):
        m = calcular_metricas_curva_s(50.0, 50.0, 100.0)
        self.assertEqual(m["spi"], 1.0)
        self.assertEqual(m["desvio_estimado"], 0.0)
        self.assertEqual(m["gap_horas"], 0.0)
        self.assertIn("NO PRAZO", m["status_text"])

    def test_calcular_metricas_curva_s_atraso_critico(self):
        # Realizado 40% vs Planejado 50% -> SPI = 0.8 -> Desvio = +25%
        m = calcular_metricas_curva_s(40.0, 50.0, 100.0)
        self.assertEqual(m["spi"], 0.8)
        self.assertEqual(m["desvio_estimado"], 25.0)
        self.assertEqual(m["gap_horas"], 25.0)
        self.assertIn("CRÍTICO", m["status_text"])

    def test_validar_alocacao_capacidade_excedida(self):
        df_ambientes = pd.DataFrame([
            {"Nome_Ambiente": "Lab 01", "Capacidade_Fisica": 20}
        ])
        df_lotacao = pd.DataFrame()

        valido, msg, _ = validar_alocacao(
            df_lotacao, df_ambientes, "Segunda", "Noite", "Lab 01", "Prof. Dione", 25
        )
        self.assertFalse(valido)
        self.assertIn("Capacidade", msg)

    def test_validar_alocacao_conflito_ambiente(self):
        df_ambientes = pd.DataFrame([
            {"Nome_Ambiente": "Lab 01", "Capacidade_Fisica": 30}
        ])
        df_lotacao = pd.DataFrame([
            {
                "Turma": "TURMA-A",
                "Dia da Semana": "Segunda",
                "Turno": "Noite",
                "Ambiente": "Lab 01",
                "Docente": "Prof. Carlos",
            }
        ])

        valido, msg, _ = validar_alocacao(
            df_lotacao, df_ambientes, "Segunda", "Noite", "Lab 01", "Prof. Dione", 15
        )
        self.assertFalse(valido)
        self.assertIn("Conflito de Ambiente", msg)

    def test_validar_alocacao_conflito_docente(self):
        df_ambientes = pd.DataFrame([
            {"Nome_Ambiente": "Lab 01", "Capacidade_Fisica": 30},
            {"Nome_Ambiente": "Lab 02", "Capacidade_Fisica": 30},
        ])
        df_lotacao = pd.DataFrame([
            {
                "Turma": "TURMA-A",
                "Dia da Semana": "Segunda",
                "Turno": "Noite",
                "Ambiente": "Lab 01",
                "Docente": "Prof. Dione",
            }
        ])

        valido, msg, _ = validar_alocacao(
            df_lotacao, df_ambientes, "Segunda", "Noite", "Lab 02", "Prof. Dione", 15
        )
        self.assertFalse(valido)
        self.assertIn("Conflito de Docente", msg)

    def test_validar_alocacao_sucesso(self):
        df_ambientes = pd.DataFrame([
            {"Nome_Ambiente": "Lab 01", "Capacidade_Fisica": 30}
        ])
        df_lotacao = pd.DataFrame()

        valido, msg, vagas = validar_alocacao(
            df_lotacao, df_ambientes, "Segunda", "Noite", "Lab 01", "Prof. Dione", 22
        )
        self.assertTrue(valido)
        self.assertEqual(msg, "")
        self.assertEqual(vagas, 8)


if __name__ == "__main__":
    unittest.main()
