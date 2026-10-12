from pathlib import Path
from io import BytesIO
import streamlit as st
from PIL import Image
from utils.ui import load_css, get_asset_path, get_project_root, render_footer

# Configuração da Página
st.set_page_config(
    page_title="Portal dos Dados - Corretor de Provas (OMR)",
    page_icon="📝",
    layout="wide",
)

# Carregamento de estilos
load_css("style.css")

# Verificação de dependências de visão computacional
try:
    import cv2
    import numpy as np
    from scipy.signal import find_peaks
    CV_AVAILABLE = True
except ImportError:
    CV_AVAILABLE = False


# ==========================================
# MOTOR DE VISÃO COMPUTACIONAL E MATEMÁTICA
# ==========================================
def processar_gabarito_por_picos(imagem_pil, gabarito_oficial, sensibilidade_pct=5.0):
    if not CV_AVAILABLE:
        return {
            "sucesso": False,
            "mensagem": "Dependências de visão computacional (OpenCV/SciPy) não encontradas no ambiente.",
        }

    try:
        # 1. Preparação da Imagem
        img = np.array(imagem_pil)
        if len(img.shape) == 3:
            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            img_gray = img

        # 2. Pré-processamento com Binarização
        _, img_bin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
        kernel = np.ones((8, 8), np.uint8)
        img_eroded = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernel)
        img_inverted = cv2.bitwise_not(img_eroded)

        # 3. Detecção das Âncoras via Projeção de Densidade
        sum_vertical = img_inverted.sum(axis=0)
        sum_horizontal = img_inverted.sum(axis=1)

        fator_sensibilidade = sensibilidade_pct / 100.0
        limite_pico_v = img_inverted.shape[0] * 255 * fator_sensibilidade
        limite_pico_h = img_inverted.shape[1] * 255 * fator_sensibilidade

        vertical_peaks, _ = find_peaks(sum_vertical, height=limite_pico_v)
        horizontal_peaks, _ = find_peaks(sum_horizontal, height=limite_pico_h)

        if len(vertical_peaks) < 2 or len(horizontal_peaks) < 2:
            return {
                "sucesso": False,
                "mensagem": "Falha na detecção das bordas do gabarito. O documento pode estar rotacionado, cortado ou com iluminação desbalanceada.",
            }

        x_inicio, x_fim = vertical_peaks[0], vertical_peaks[-1]
        y_inicio, y_fim = horizontal_peaks[0], horizontal_peaks[-1]

        # Recorte da Região de Interesse (ROI)
        grade = img_inverted[y_inicio:y_fim, x_inicio:x_fim]

        # 4. Fatiamento Matemático e Extração
        qtd_questoes = len(gabarito_oficial)
        qtd_alternativas = 5

        altura_grade = (grade.shape[0] // qtd_questoes) * qtd_questoes
        largura_grade = (grade.shape[1] // qtd_alternativas) * qtd_alternativas
        grade_redimensionada = cv2.resize(grade, (largura_grade, altura_grade))

        linhas = np.vsplit(grade_redimensionada, qtd_questoes)

        respostas_aluno = []
        mapa_letras = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
        nota = 0
        detalhes = []

        for i, linha in enumerate(linhas):
            alternativas = np.hsplit(linha, qtd_alternativas)
            pixels_por_alt = [cv2.countNonZero(alt) for alt in alternativas]
            max_pixels = max(pixels_por_alt)

            area_celula = (altura_grade // qtd_questoes) * (
                largura_grade // qtd_alternativas
            )
            if max_pixels < (area_celula * 0.10):
                respostas_aluno.append(-1)
                detalhes.append(f"Q{i+1:02d}: Em branco (Gabarito: {gabarito_oficial[i]})")
            else:
                indice_marcado = pixels_por_alt.index(max_pixels)
                letra_marcada = mapa_letras[indice_marcado]
                respostas_aluno.append(letra_marcada)

                if letra_marcada == gabarito_oficial[i]:
                    nota += 1
                    detalhes.append(f"Q{i+1:02d}: Correta ({letra_marcada})")
                else:
                    detalhes.append(
                        f"Q{i+1:02d}: Incorreta (Marcou {letra_marcada}, Gabarito: {gabarito_oficial[i]})"
                    )

        # 5. Imagem de Auditoria com linhas de ancoragem
        img_auditoria = cv2.cvtColor(img_inverted, cv2.COLOR_GRAY2RGB)
        cv2.line(img_auditoria, (x_inicio, 0), (x_inicio, img_inverted.shape[0]), (255, 0, 0), 3)
        cv2.line(img_auditoria, (x_fim, 0), (x_fim, img_inverted.shape[0]), (255, 0, 0), 3)
        cv2.line(img_auditoria, (0, y_inicio), (img_inverted.shape[1], y_inicio), (0, 255, 0), 3)
        cv2.line(img_auditoria, (0, y_fim), (img_inverted.shape[1], y_fim), (0, 255, 0), 3)

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
st.title("📝 Corretor de Provas Óptico (OMR com Visão Computacional)")
st.markdown(
    "Sistema de leitura e correção automatizada de folhas de respostas utilizando "
    "projeção de perfis de densidade, filtros morfológicos e OpenCV."
)
st.divider()

if not CV_AVAILABLE:
    st.warning("⚠️ As bibliotecas `opencv-python` e `scipy` são necessárias para o processamento de imagens do corretor OMR.")

col_cfg, col_up = st.columns([1, 1], gap="large")

with col_cfg:
    st.subheader("1. Configurações da Prova")
    gabarito_input = st.text_input("Gabarito Oficial (Ex: ABCDEABCDE):", "ABCDEABCDE").upper()
    gabarito_limpo = "".join([c for c in gabarito_input if c in "ABCDE"])

    st.info(f"Total de questões configuradas no gabarito: **{len(gabarito_limpo)}**")

    sensibilidade = st.slider(
        "Sensibilidade de Detecção de Margem (%)",
        min_value=2.0,
        max_value=12.0,
        value=5.0,
        step=0.5,
        help="Ajuste fino caso a câmera tenha gerado sombras ou iluminação não uniforme.",
    )

    # Geração Dinâmica da Folha de Respostas em PDF
    st.markdown("#### 📄 Gerador de Folha de Respostas")
    try:
        from gerador_gabarito import gerar_gabarito_pdf
        pdf_bytes = gerar_gabarito_pdf(None, qtd_questoes=max(5, len(gabarito_limpo)))
        st.download_button(
            label=f"📥 Baixar Folha de Respostas ({max(5, len(gabarito_limpo))} Questões)",
            data=pdf_bytes,
            file_name=f"Gabarito_OMR_{max(5, len(gabarito_limpo))}_Questoes.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except Exception:
        # Fallback para o arquivo estático caso ReportLab não esteja disponível
        gabarito_pdf_path = get_project_root() / "Gabarito_OMR_Padrao.pdf"
        if gabarito_pdf_path.exists():
            with open(gabarito_pdf_path, "rb") as f_pdf:
                st.download_button(
                    label="📄 Baixar Folha Padrão Pré-gerada (PDF)",
                    data=f_pdf.read(),
                    file_name="Gabarito_OMR_Padrao.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

with col_up:
    st.subheader("2. Upload da Imagem")
    upload = st.file_uploader(
        "Faça o upload do documento digitalizado",
        type=["png", "jpg", "jpeg"],
        help="A folha de respostas deve estar bem iluminada e sem rotação acentuada.",
    )

st.write("")
if upload is not None and st.button("🚀 Executar Correção", type="primary", use_container_width=True):
    if len(gabarito_limpo) == 0:
        st.error("Por favor, informe ao menos uma questão no gabarito oficial.")
    else:
        with st.spinner("Analisando imagem e rastreando picos de densidade..."):
            imagem = Image.open(upload)
            resultado = processar_gabarito_por_picos(imagem, gabarito_limpo, sensibilidade_pct=sensibilidade)

            if resultado["sucesso"]:
                porcentagem = (resultado["nota"] / resultado["total"]) * 100
                st.success(f"Nota Final: **{resultado['nota']} / {resultado['total']}** ({porcentagem:.1f}%)")

                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    st.markdown("#### Detalhes por Questão:")
                    st.code(resultado["detalhes"])
                with col_res2:
                    st.markdown("#### Auditoria de Corte (Bordas Detectadas):")
                    st.image(
                        resultado["auditoria"],
                        caption="Linhas de Corte Identificadas",
                        use_container_width=True,
                    )
            else:
                st.error(resultado["mensagem"])

render_footer()
