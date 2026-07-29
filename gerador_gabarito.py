"""
Script para gerar o PDF do Gabarito Oficial.
Utiliza ReportLab para garantir precisão geométrica na impressão.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


def gerar_gabarito_pdf(nome_arquivo="Gabarito_OMR_Padrao.pdf", qtd_questoes=10):
    # Inicializa o canvas do PDF no formato A4
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    # ---------------------------------------------------------------------
    # 1. CABEÇALHO (FORA DA ÁREA DE LEITURA DO OPENCV)
    # ---------------------------------------------------------------------
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, altura - 2.5 * cm, "FOLHA DE RESPOSTAS OFICIAL")

    c.setFont("Helvetica", 12)
    c.drawString(
        2 * cm,
        altura - 3.5 * cm,
        "Nome: ________________________________________________________",
    )
    c.drawString(2 * cm, altura - 4.5 * cm, "Data: ___/___/202__")

    # ---------------------------------------------------------------------
    # 2. RETÂNGULO DE ANCORAGEM (ESSENCIAL PARA O ALINHAMENTO)
    # ---------------------------------------------------------------------
    # Definição das margens e tamanho do quadro de leitura
    margem_esq = 3 * cm
    margem_inf = 5 * cm
    largura_retangulo = 15 * cm
    altura_retangulo = 16 * cm

    # Desenha a linha externa grossa para detecção do OpenCV
    c.setLineWidth(3)
    c.rect(margem_esq, margem_inf, largura_retangulo, altura_retangulo)

    # ---------------------------------------------------------------------
    # 3. GRADE INTERNA (QUESTÕES E BOLINHAS)
    # ---------------------------------------------------------------------
    c.setLineWidth(1)
    c.setFont("Helvetica-Bold", 10)

    # Calcula o espaçamento exato entre as linhas e colunas
    passo_y = altura_retangulo / (qtd_questoes + 1)
    passo_x = largura_retangulo / 6

    # Desenha os cabeçalhos das colunas (A, B, C, D, E)
    letras = ["A", "B", "C", "D", "E"]
    for j, letra in enumerate(letras):
        # Calcula a posição X centralizada para cada letra
        x_letra = margem_esq + passo_x * (j + 1) + (passo_x / 2) - 0.15 * cm
        y_letra = margem_inf + altura_retangulo - (passo_y / 2) - 0.15 * cm
        c.drawString(x_letra, y_letra, letra)

    # Desenha as numerações e as alternativas (círculos)
    c.setFont("Helvetica", 10)
    for i in range(qtd_questoes):
        # O eixo Y do ReportLab começa embaixo (0) e sobe.
        y_linha = margem_inf + altura_retangulo - passo_y * (i + 2)

        # Imprime o número da questão (ex: Q01)
        c.drawString(margem_esq + 0.5 * cm, y_linha + 0.5 * cm, f"Q{i+1:02d}")

        # Desenha 5 círculos por questão
        for j in range(5):
            x_centro = margem_esq + passo_x * (j + 1) + (passo_x / 2)
            y_centro = y_linha + 0.65 * cm

            # Desenha a bolinha (raio de 0.35 cm)
            c.circle(x_centro, y_centro, 0.35 * cm)

    # Salva e gera o arquivo físico
    c.save()
    print(f"Arquivo '{nome_arquivo}' gerado com sucesso.")


# Executa a função definindo 10 questões como padrão
if __name__ == "__main__":
    gerar_gabarito_pdf(qtd_questoes=10)
