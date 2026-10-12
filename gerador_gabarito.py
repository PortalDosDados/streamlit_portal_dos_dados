"""
Módulo para geração do PDF do Gabarito Oficial de Provas (OMR).
Utiliza ReportLab para garantir precisão geométrica na impressão e calibração com OpenCV.
"""

from io import BytesIO
from typing import Union


def gerar_gabarito_pdf(destino: Union[str, BytesIO, None] = None, qtd_questoes: int = 10) -> bytes:
    """
    Gera o PDF de folha de respostas com grade milimetricamente alinhada.
    Se 'destino' for None, retorna os bytes do PDF em memória.
    Se 'destino' for string, salva no arquivo físico e também retorna os bytes.
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
    except ImportError as e:
        raise ImportError(
            "O pacote 'reportlab' é necessário para gerar folhas de respostas em PDF. "
            "Instale-o via 'pip install reportlab'."
        ) from e

    # Gerenciamento de buffer em memória ou arquivo
    buffer = BytesIO()
    alvo = buffer if (destino is None or isinstance(destino, BytesIO)) else destino

    c = canvas.Canvas(alvo, pagesize=A4)
    largura, altura = A4

    # 1. CABEÇALHO (fora do retângulo de leitura do OMR)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, altura - 2.5 * cm, "FOLHA DE RESPOSTAS OFICIAL")

    c.setFont("Helvetica", 11)
    c.drawString(
        2 * cm,
        altura - 3.5 * cm,
        "Nome: ________________________________________________________",
    )
    c.drawString(2 * cm, altura - 4.3 * cm, "Data: ___/___/202__")
    c.drawString(12 * cm, altura - 4.3 * cm, f"Total de Questões: {qtd_questoes:02d}")

    # 2. RETÂNGULO DE ANCORAGEM (Linha externa grossa para OpenCV)
    margem_esq = 3 * cm
    margem_inf = 4.5 * cm
    largura_retangulo = 15 * cm
    altura_retangulo = 17 * cm

    c.setLineWidth(3)
    c.rect(margem_esq, margem_inf, largura_retangulo, altura_retangulo)

    # 3. GRADE INTERNA (Cabeçalho de Colunas e Alternativas)
    c.setLineWidth(1)
    c.setFont("Helvetica-Bold", 10)

    passo_y = altura_retangulo / (qtd_questoes + 1)
    passo_x = largura_retangulo / 6

    letras = ["A", "B", "C", "D", "E"]
    for j, letra in enumerate(letras):
        x_letra = margem_esq + passo_x * (j + 1) + (passo_x / 2) - 0.15 * cm
        y_letra = margem_inf + altura_retangulo - (passo_y / 2) - 0.15 * cm
        c.drawString(x_letra, y_letra, letra)

    c.setFont("Helvetica", 9)
    for i in range(qtd_questoes):
        y_linha = margem_inf + altura_retangulo - passo_y * (i + 2)

        # Rótulo da Questão
        c.drawString(margem_esq + 0.5 * cm, y_linha + 0.45 * cm, f"Q{i+1:02d}")

        # Círculos das Alternativas (5 opções)
        for j in range(5):
            x_centro = margem_esq + passo_x * (j + 1) + (passo_x / 2)
            y_centro = y_linha + 0.58 * cm
            c.circle(x_centro, y_centro, 0.32 * cm)

    c.save()

    if isinstance(destino, str):
        with open(destino, "wb") as f:
            f.write(buffer.getvalue())
        return buffer.getvalue()
    elif isinstance(destino, BytesIO):
        return destino.getvalue()

    return buffer.getvalue()


if __name__ == "__main__":
    gerar_gabarito_pdf("Gabarito_OMR_Padrao.pdf", qtd_questoes=10)
    print("Gabarito gerado com sucesso!")
