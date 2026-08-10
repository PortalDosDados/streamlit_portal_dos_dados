import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# =============================================================================
# 1. FUNÇÕES AUXILIARES (GEOMETRIA E ORDENAÇÃO)
# =============================================================================


def ordenar_pontos(pontos):
    """Ordena 4 pontos na ordem: Top-Left, Top-Right, Bottom-Right, Bottom-Left."""
    pontos = pontos.reshape((4, 2))
    pontos_novos = np.zeros((4, 2), dtype=np.float32)
    soma = pontos.sum(axis=1)
    pontos_novos[0] = pontos[np.argmin(soma)]
    pontos_novos[2] = pontos[np.argmax(soma)]  # Bottom-Right
    diferenca = np.diff(pontos, axis=1)
    pontos_novos[1] = pontos[np.argmin(diferenca)]  # Top-Right
    pontos_novos[3] = pontos[np.argmax(diferenca)]  # Bottom-Left
    return pontos_novos


def ordenar_contornos(cnts, method="esquerda-para-direita"):
    """
    Ordena uma lista de contornos espacialmente.
    Baseado na implementação clássica do imutils.
    """
    reverse = False
    i = 0
    if method == "direita-para-esquerda" or method == "baixo-para-cima":
        reverse = True
    if method == "cima-para-baixo" or method == "baixo-para-cima":
        i = 1

    caixas = [cv2.boundingRect(c) for c in cnts]
    cnts, caixas = zip(
        *sorted(zip(cnts, caixas), key=lambda b: b[1][i], reverse=reverse)
    )
    return list(cnts)


# =============================================================================
# 2. LÓGICA DE VISÃO COMPUTACIONAL (PIPELINE OMR CLÁSSICO)
# =============================================================================


def processar_imagem_opencv(imagem_pil, gabarito_oficial):
    try:
        # 1. Preparação da Imagem
        img = np.array(imagem_pil)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Redimensionamento para padronizar o processamento
        r = 800.0 / img.shape[1]
        dim = (800, int(img.shape[0] * r))
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        img_original = img.copy()

        # 2. Detecção de Bordas (Canny)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)

        # 3. Encontrar o contorno principal (Retângulo da grade de questões)
        contornos, _ = cv2.findContours(
            edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if not contornos:
            return {
                "sucesso": False,
                "mensagem": "Nenhum contorno encontrado na imagem.",
            }

        # Ordena pelos maiores contornos
        contornos = sorted(contornos, key=cv2.contourArea, reverse=True)
        contorno_documento = None

        for c in contornos:
            perimetro = cv2.arcLength(c, True)
            aproximacao = cv2.approxPolyDP(c, 0.02 * perimetro, True)

            # Se o contorno tem 4 pontas, assumimos que é o retângulo da prova
            if len(aproximacao) == 4:
                contorno_documento = aproximacao
                break

        if contorno_documento is None:
            return {
                "sucesso": False,
                "mensagem": "Erro: Não foi possível identificar o quadro delimitador da prova. Certifique-se de que o retângulo impresso está totalmente visível.",
            }

        # 4. Alinhamento (Bird's Eye View)
        pontos_papel = ordenar_pontos(contorno_documento)

        # Define o tamanho do documento planificado (600x800)
        largura_doc, altura_doc = 600, 800
        pontos_destino = np.float32(
            [[0, 0], [largura_doc, 0], [largura_doc, altura_doc], [0, altura_doc]]
        )

        matriz = cv2.getPerspectiveTransform(pontos_papel, pontos_destino)
        warped = cv2.warpPerspective(gray, matriz, (largura_doc, altura_doc))
        warped_color = cv2.warpPerspective(
            img_original, matriz, (largura_doc, altura_doc)
        )

        # 5. Binarização (Destacar a tinta da caneta)
        _, thresh = cv2.threshold(
            warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )

        # 6. Filtragem geométrica: Encontrar apenas os Círculos (Bolinhas)
        cnts, _ = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        bolinhas = []

        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            aspect_ratio = w / float(h)

            # Uma bolinha deve ter largura e altura adequadas e proporção próxima de 1.0 (quadrado/círculo)
            if w >= 15 and h >= 15 and 0.8 <= aspect_ratio <= 1.2:
                bolinhas.append(c)

        qtd_questoes = len(gabarito_oficial)
        total_bolinhas_esperadas = qtd_questoes * 5

        # Verificação de segurança estrutural da abordagem
        if len(bolinhas) != total_bolinhas_esperadas:
            return {
                "sucesso": False,
                "mensagem": f"Erro de leitura OMR: Esperadas {total_bolinhas_esperadas} bolinhas, mas o algoritmo encontrou {len(bolinhas)}. A foto pode estar desfocada ou mal iluminada, impedindo a detecção de alguns círculos.",
            }

        # 7. Avaliação e Correção
        bolinhas = ordenar_contornos(bolinhas, method="cima-para-baixo")
        mapa_letras = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
        nota = 0
        detalhes_correcao = []

        for q, i in enumerate(np.arange(0, len(bolinhas), 5)):
            # Pega as 5 bolinhas da questão e ordena da esquerda para a direita
            cnts_questao = ordenar_contornos(
                bolinhas[i : i + 5], method="esquerda-para-direita"
            )
            pixels_marcados = []

            letra_gabarito = gabarito_oficial[q]

            for j, c in enumerate(cnts_questao):
                # Cria uma máscara que contém apenas a bolinha atual
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)

                # Conta quantos pixels brancos (tinta preta do papel) existem dentro da bolinha
                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                total_pixels = cv2.countNonZero(mask)
                pixels_marcados.append(total_pixels)

            max_pixels = max(pixels_marcados)

            # Se a alternativa com mais pixels não atingir um limiar mínimo, considera em branco
            if max_pixels < 50:
                detalhes_correcao.append(
                    f"Q{q+1}: Incorreta (Em branco, correta era {letra_gabarito})"
                )
            else:
                indice_marcado = pixels_marcados.index(max_pixels)
                letra_aluno = mapa_letras[indice_marcado]

                # Desenha o resultado na imagem para auditoria
                cor = (0, 255, 0) if letra_aluno == letra_gabarito else (0, 0, 255)
                cv2.drawContours(
                    warped_color, [cnts_questao[indice_marcado]], -1, cor, 2
                )

                if letra_aluno == letra_gabarito:
                    nota += 1
                    detalhes_correcao.append(f"Q{q+1}: Correta (Marcou {letra_aluno})")
                else:
                    detalhes_correcao.append(
                        f"Q{q+1}: Incorreta (Marcou {letra_aluno}, correta era {letra_gabarito})"
                    )

        return {
            "sucesso": True,
            "nota": nota,
            "total": qtd_questoes,
            "detalhes": "\n".join(detalhes_correcao),
            "img_alinhada": cv2.cvtColor(warped_color, cv2.COLOR_BGR2RGB),
        }

    except Exception as e:
        return {
            "sucesso": False,
            "mensagem": f"Erro técnico no processamento: {str(e)}",
        }


# =============================================================================
# 3. GERAÇÃO DE GABARITO (REPORTLAB - ADAPTADO PARA OMR CLÁSSICO)
# =============================================================================


def gerar_gabarito_pdf(qtd_questoes):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4
    margem = 40

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(largura / 2, altura - 30, "Gabarito - Padrão OMR")

    c.setFont("Helvetica", 11)
    c.drawString(
        margem,
        altura - 60,
        "Nome: ___________________________________________________________",
    )

    # ---------------------------------------------------------
    # A ÂNCORA DO ALGORITMO: O Retângulo Delimitador
    # O OpenCV vai procurar exatamente este quadrado para alinhar a imagem
    # ---------------------------------------------------------
    topo_retangulo = altura - 90
    base_retangulo = margem
    c.setLineWidth(2)
    c.rect(
        margem,
        base_retangulo,
        largura - (2 * margem),
        topo_retangulo - base_retangulo,
        stroke=1,
        fill=0,
    )
    # ---------------------------------------------------------

    c.setLineWidth(1)
    x_inicio = margem + 20
    y_atual = topo_retangulo - 30

    alternativas = ["A", "B", "C", "D", "E"]

    for q in range(qtd_questoes):
        c.setFont("Helvetica", 10)
        c.drawString(x_inicio, y_atual - 4, f"{q+1:02d}.")

        for alt_idx, letra in enumerate(alternativas):
            # Espaçamento fixo garantido
            x_bolinha = x_inicio + 40 + (alt_idx * 30)

            # Círculos com linha levemente mais grossa (1.5) ajudam o algoritmo Canny
            c.setLineWidth(1.5)
            c.circle(x_bolinha, y_atual, 8, stroke=1, fill=0)

            c.setFont("Helvetica", 8)
            c.drawCentredString(x_bolinha, y_atual - 3, letra)

        y_atual -= 30

        # Controle simples de coluna (cria nova coluna se faltar espaço)
        if y_atual < base_retangulo + 30:
            y_atual = topo_retangulo - 30
            x_inicio += 200

    c.save()
    buffer.seek(0)
    return buffer


# =============================================================================
# 4. INTERFACE DO USUÁRIO (FRONT-END STREAMLIT)
# =============================================================================

st.title("🎯 Corretor OMR Clássico")
st.markdown(
    "Implementação baseada no pipeline clássico (Extração de Borda + Filtro de Contorno)."
)

if "corretor_gabarito_salvo" not in st.session_state:
    st.session_state.corretor_gabarito_salvo = []
if "corretor_qtd_questoes" not in st.session_state:
    st.session_state.corretor_qtd_questoes = 10

col_config, col_captura = st.columns([1, 2])

with col_config:
    st.subheader("1. Configuração")
    st.session_state.corretor_qtd_questoes = st.number_input(
        "Quantidade de Questões",
        min_value=1,
        max_value=50,
        value=st.session_state.corretor_qtd_questoes,
    )

    gabarito_input = st.text_input(
        "Gabarito (Ex: ABCDE)", max_chars=st.session_state.corretor_qtd_questoes
    ).upper()

    if st.button("Salvar Gabarito", type="primary"):
        gabarito_limpo = "".join([c for c in gabarito_input if c in "ABCDE"])
        if len(gabarito_limpo) == st.session_state.corretor_qtd_questoes:
            st.session_state.corretor_gabarito_salvo = list(gabarito_limpo)
            st.success("Gabarito salvo!")
        else:
            st.error(
                f"Erro: Digite exatamente {st.session_state.corretor_qtd_questoes} letras válidas."
            )

    if st.session_state.corretor_gabarito_salvo:
        st.info(f"**Ativo:** {' - '.join(st.session_state.corretor_gabarito_salvo)}")
        if st.button("Resetar Memória"):
            st.session_state.corretor_gabarito_salvo = []
            st.rerun()

    st.markdown("---")
    st.subheader("2. Gerar Folha Padrão")
    st.warning(
        "Gere e utilize este NOVO PDF. O retângulo delimitador é exigência deste algoritmo."
    )
    pdf_buffer = gerar_gabarito_pdf(st.session_state.corretor_qtd_questoes)
    st.download_button(
        label="📄 Baixar Novo PDF",
        data=pdf_buffer,
        file_name="gabarito_omr_classico.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True,
    )

with col_captura:
    st.subheader("3. Correção")
    if not st.session_state.corretor_gabarito_salvo:
        st.warning("Configure o gabarito oficial na coluna lateral.")
    else:
        metodo_entrada = st.radio(
            "Método de Entrada:", ["Câmera", "Arquivo"], horizontal=True
        )

        imagem_carregada = None
        if metodo_entrada == "Câmera":
            imagem_carregada = st.camera_input(
                "Fotografe garantindo que o retângulo preto da folha esteja totalmente visível"
            )
        else:
            imagem_carregada = st.file_uploader(
                "Upload da foto (.jpg/.png)", type=["jpg", "png"]
            )

        if imagem_carregada and st.button(
            "Executar Correção", type="primary", use_container_width=True
        ):
            with st.spinner("Aplicando filtros OMR..."):
                img = Image.open(imagem_carregada)
                resultado = processar_imagem_opencv(
                    img, st.session_state.corretor_gabarito_salvo
                )

                if resultado.get("sucesso"):
                    st.success("Operação concluída!")
                    st.metric(
                        label="Nota Calculada",
                        value=f"{resultado['nota']} / {resultado['total']}",
                    )

                    with st.expander("Log Analítico", expanded=True):
                        st.text(resultado["detalhes"])

                    st.markdown("### Auditoria OMR")
                    st.image(resultado["img_alinhada"], use_container_width=True)
                else:
                    st.error(resultado["mensagem"])
