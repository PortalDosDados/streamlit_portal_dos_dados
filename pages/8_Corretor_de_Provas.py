import streamlit as st
import cv2
import numpy as np
from scipy.signal import find_peaks
from PIL import Image


# ==========================================
# MOTOR DE VISÃO COMPUTACIONAL E MATEMÁTICA
# ==========================================
def processar_gabarito_por_picos(imagem_pil, gabarito_oficial):
    try:
        # 1. Preparação da Imagem
        img = np.array(imagem_pil)
        if len(img.shape) == 3:
            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            img_gray = img

        # 2. Pré-processamento exato do notebook
        # Binarização com limite estático em 127
        _, img_bin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

        # Operação morfológica (Fechamento) para aglutinar formas
        kernel = np.ones((8, 8), np.uint8)
        img_eroded = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernel)

        # Inversão: O fundo branco fica 0 e a tinta preta vira 255 para permitir a soma
        img_inverted = cv2.bitwise_not(img_eroded)

        # 3. Deteção das Âncoras via Projeção
        # Soma ao longo do eixo X (colunas) e Y (linhas)
        sum_vertical = img_inverted.sum(axis=0)
        sum_horizontal = img_inverted.sum(axis=1)

        # O parâmetro 'height' é usado para filtrar pequenos ruídos que não são margens reais
        limite_pico_v = img_inverted.shape[0] * 255 * 0.05
        limite_pico_h = img_inverted.shape[1] * 255 * 0.05

        vertical_peaks, _ = find_peaks(sum_vertical, height=limite_pico_v)
        horizontal_peaks, _ = find_peaks(sum_horizontal, height=limite_pico_h)

        # Validação de segurança: Precisamos de pelo menos 2 picos (início e fim) por eixo
        if len(vertical_peaks) < 2 or len(horizontal_peaks) < 2:
            return {
                "sucesso": False,
                "mensagem": "Falha na deteção de margens. O documento pode estar torto ou com muito ruído no fundo.",
            }

        # 4. Definir Coordenadas de Recorte
        # O primeiro e último pico de cada eixo definem a caixa delimitadora do gabarito
        x_inicio, x_fim = vertical_peaks[0], vertical_peaks[-1]
        y_inicio, y_fim = horizontal_peaks[0], horizontal_peaks[-1]

        # Recorte da Região de Interesse (ROI)
        grade = img_inverted[y_inicio:y_fim, x_inicio:x_fim]

        # 5. Fatiamento Matemático e Extração
        qtd_questoes = len(gabarito_oficial)
        qtd_alternativas = 5

        # Redimensionamento para forçar a matriz a ser perfeitamente divisível pelo número de questões/alternativas
        altura_grade = (grade.shape[0] // qtd_questoes) * qtd_questoes
        largura_grade = (grade.shape[1] // qtd_alternativas) * qtd_alternativas
        grade_redimensionada = cv2.resize(grade, (largura_grade, altura_grade))

        # Fatiar a grade em linhas (Questões)
        linhas = np.vsplit(grade_redimensionada, qtd_questoes)

        respostas_aluno = []
        mapa_letras = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
        nota = 0
        detalhes = []

        # Analisar cada questão
        for i, linha in enumerate(linhas):
            # Fatiar a linha em colunas (Alternativas A, B, C, D, E)
            alternativas = np.hsplit(linha, qtd_alternativas)

            # Contabilizar os pixels de tinta (brancos na imagem invertida) em cada alternativa
            pixels_por_alt = [cv2.countNonZero(alt) for alt in alternativas]
            max_pixels = max(pixels_por_alt)

            # Definir um limite mínimo de tinta (10% da área da célula) para ignorar rabiscos leves
            area_celula = (altura_grade // qtd_questoes) * (
                largura_grade // qtd_alternativas
            )
            if max_pixels < (area_celula * 0.10):
                respostas_aluno.append(-1)
                detalhes.append(f"Q{i+1}: Em branco (Gabarito: {gabarito_oficial[i]})")
            else:
                indice_marcado = pixels_por_alt.index(max_pixels)
                letra_marcada = mapa_letras[indice_marcado]
                respostas_aluno.append(letra_marcada)

                # Corrigir a resposta
                if letra_marcada == gabarito_oficial[i]:
                    nota += 1
                    detalhes.append(f"Q{i+1}: Correta ({letra_marcada})")
                else:
                    detalhes.append(
                        f"Q{i+1}: Incorreta (Marcou {letra_marcada}, Gabarito: {gabarito_oficial[i]})"
                    )

        # 6. Preparação da Imagem de Auditoria
        # Converte de volta para cor para desenhar as linhas de corte em evidência
        img_auditoria = cv2.cvtColor(img_inverted, cv2.COLOR_GRAY2RGB)

        # Desenhar margens verticais (Azul) e horizontais (Verde) encontradas pelos picos
        cv2.line(
            img_auditoria,
            (x_inicio, 0),
            (x_inicio, img_inverted.shape[0]),
            (255, 0, 0),
            3,
        )
        cv2.line(
            img_auditoria, (x_fim, 0), (x_fim, img_inverted.shape[0]), (255, 0, 0), 3
        )
        cv2.line(
            img_auditoria,
            (0, y_inicio),
            (img_inverted.shape[1], y_inicio),
            (0, 255, 0),
            3,
        )
        cv2.line(
            img_auditoria, (0, y_fim), (img_inverted.shape[1], y_fim), (0, 255, 0), 3
        )

        return {
            "sucesso": True,
            "nota": nota,
            "total": qtd_questoes,
            "detalhes": "\n".join(detalhes),
            "auditoria": img_auditoria,
        }

    except Exception as e:
        return {
            "sucesso": False,
            "mensagem": f"Erro interno de processamento de matriz: {str(e)}",
        }


# ==========================================
# INTERFACE GRÁFICA STREAMLIT
# ==========================================
st.title("Corretor via Projeção de Perfis (SciPy)")
st.markdown(
    "Implementação baseada no rastreamento de picos de densidade da matriz da imagem."
)

gabarito_input = st.text_input("Gabarito Oficial (Ex: ABCDE)", "ABCDE").upper()
gabarito_limpo = "".join([c for c in gabarito_input if c in "ABCDE"])

upload = st.file_uploader("Faça o upload do documento", type=["png", "jpg", "jpeg"])
st.warning("O documento digitalizado deve estar reto, sem rotação.")

if upload is not None and st.button("Executar Correção"):
    if len(gabarito_limpo) == 0:
        st.error("Por favor, insira um gabarito válido.")
    else:
        with st.spinner("Processando..."):
            imagem = Image.open(upload)
            resultado = processar_gabarito_por_picos(imagem, gabarito_limpo)

            if resultado["sucesso"]:
                st.success(f"Nota Final: {resultado['nota']} / {resultado['total']}")

                col1, col2 = st.columns(2)
                with col1:
                    st.text("Detalhes da Correção:")
                    st.text(resultado["detalhes"])
                with col2:
                    st.image(
                        resultado["auditoria"],
                        caption="Linhas de Corte Identificadas",
                        use_container_width=True,
                    )
            else:
                st.error(resultado["mensagem"])
