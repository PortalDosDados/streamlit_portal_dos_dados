"""
Regras de negócio, cálculos matemáticos e validações da aplicação.
Funções puras sem dependência direta de contexto de sessão do Streamlit,
facilitando reuso e testes unitários automatizados.
"""

from datetime import time
from typing import Optional, Tuple, Dict, Any
import pandas as pd


def parse_horario(valor: Any) -> Tuple[Optional[time], str]:
    """
    Interpreta entradas de horário em diversos formatos comuns (HHMM, HMM, HH, HH:MM)
    e converte para objeto datetime.time e string formatada.
    """
    if not valor:
        return None, ""

    nums = "".join(filter(str.isdigit, str(valor)))

    try:
        if len(nums) == 4:  # Formato HHMM (ex: 1430)
            h, m = int(nums[:2]), int(nums[2:])
        elif len(nums) == 3:  # Formato HMM (ex: 830 -> 08:30)
            h, m = int(nums[:1]), int(nums[1:])
        elif len(nums) <= 2 and nums != "":  # Formato HH (ex: 14 -> 14:00)
            h, m = int(nums), 0
        else:
            return None, str(valor)

        if 0 <= h <= 23 and 0 <= m <= 59:
            return time(h, m), f"{h:02d}:{m:02d}"

        return None, str(valor)
    except Exception:
        return None, str(valor)


def classificar_severidade_parada(horas_decimais: float) -> Tuple[str, str]:
    """
    Retorna o texto de ação recomendada e a cor do alerta com base na duração da parada.
    """
    if horas_decimais > 1.5:
        return "REALIZAR ANÁLISE DE FALHA (CRÍTICA)", "#ef5350"
    elif horas_decimais > 1.0:
        return "REALIZAR ANÁLISE FCA (FATO, CAUSA, AÇÃO)", "#ffa726"
    else:
        return "APONTAMENTO PADRÃO NO RELATÓRIO DE TURNO", "#66bb6a"


def calcular_metricas_curva_s(
    percentual_realizado: float,
    percentual_planejado: float,
    total_duracao_planejada: float,
) -> Dict[str, Any]:
    """
    Calcula os indicadores de Valor Agregado (EVM):
    - SPI (Schedule Performance Index)
    - Desvio Estimado (%)
    - Gap de Horas projetado
    - Status e cor visual
    """
    if percentual_planejado > 0:
        spi = percentual_realizado / percentual_planejado
    else:
        spi = 1.0

    if spi > 0:
        desvio_estimado = (100.0 / spi) - 100.0
        estimativa_horas_total = total_duracao_planejada / spi
    else:
        desvio_estimado = 0.0
        estimativa_horas_total = total_duracao_planejada

    gap_horas = estimativa_horas_total - total_duracao_planejada

    if desvio_estimado > 15:
        status_text, cor_status = "🔴 CRÍTICO / ATRASO", "#ef5350"
    elif desvio_estimado > 5:
        status_text, cor_status = "⚠️ POTENCIAL ATRASO", "#ffa726"
    else:
        status_text, cor_status = "✅ NO PRAZO", "#66bb6a"

    return {
        "spi": round(spi, 2),
        "desvio_estimado": round(desvio_estimado, 2),
        "gap_horas": round(gap_horas, 2),
        "status_text": status_text,
        "cor_status": cor_status,
    }


def validar_alocacao(
    df_lotacao: pd.DataFrame,
    df_ambientes: pd.DataFrame,
    dia: str,
    turno: str,
    ambiente: str,
    docente: str,
    alunos_alocados: int,
) -> Tuple[bool, str, int]:
    """
    Valida as restrições operacionais de uma nova alocação:
    1. Capacidade máxima física do ambiente.
    2. Conflito de ocupação do ambiente no mesmo dia e turno.
    3. Conflito de ocupação do docente no mesmo dia e turno.

    Retorna: (sucesso: bool, mensagem_erro: str, vagas_remanescentes: int)
    """
    # 1. Capacidade do ambiente
    filtro_amb = df_ambientes[df_ambientes["Nome_Ambiente"] == ambiente]
    if filtro_amb.empty:
        return False, f"Ambiente '{ambiente}' não cadastrado.", 0

    cap_max = int(filtro_amb.iloc[0]["Capacidade_Fisica"])
    if alunos_alocados > cap_max:
        return (
            False,
            f"Erro de Capacidade: O ambiente '{ambiente}' suporta até {cap_max} alunos.",
            0,
        )

    # 2. Conflito de ambiente
    if not df_lotacao.empty:
        conflito_amb = df_lotacao[
            (df_lotacao["Dia da Semana"] == dia)
            & (df_lotacao["Turno"] == turno)
            & (df_lotacao["Ambiente"] == ambiente)
        ]
        if not conflito_amb.empty:
            turma_conflito = conflito_amb.iloc[0]["Turma"]
            return (
                False,
                f"Conflito de Ambiente: O espaço '{ambiente}' já está alocado para a turma '{turma_conflito}' na {dia} ({turno}).",
                0,
            )

        # 3. Conflito de docente
        conflito_doc = df_lotacao[
            (df_lotacao["Dia da Semana"] == dia)
            & (df_lotacao["Turno"] == turno)
            & (df_lotacao["Docente"] == docente)
        ]
        if not conflito_doc.empty:
            turma_conflito = conflito_doc.iloc[0]["Turma"]
            return (
                False,
                f"Conflito de Docente: O professor '{docente}' já possui aula atribuída com a turma '{turma_conflito}' na {dia} ({turno}).",
                0,
            )

    vagas = max(0, cap_max - int(alunos_alocados))
    return True, "", vagas
