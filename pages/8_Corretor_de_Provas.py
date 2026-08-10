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
# 1. FUNÇÕES AUXILIARES (GEOMETRIA)
# =============================================================================


def ordenar_pontos(pontos):
    pontos = pontos.reshape((4, 2))
    pontos_novos = np.zeros((4, 2), dtype=np.float32)

    soma = pontos.sum(axis=1)
    pontos_novos[0] = pontos[np.argmin(soma)]
    pontos_novos[3] = pontos[np.argmax(soma)]

    diferenca = np.diff(pontos, axis=1)
    pontos_novos[1] = pontos[np.argmin(diferenca)]
    pontos_novos[2] = pontos[np.argmax(diferenca)]

    return pontos_novos


def ordenar_contornos_esquerda_direita(contornos):
    """Ordena uma lista de contornos baseada na coordenada X (esquerda para a direita)."""
    caixas = [cv2.boundingRect(c) for c in contornos]
    contornos_ordenados, _ = zip(*sorted(zip(contornos, caixas), key=lambda b: b[1][0]))
    return list(contornos_ordenados)


def ordenar_contornos_cima_baixo(contornos):
    """Ordena uma lista de contornos baseada na coordenada Y (cima para baixo)."""
    caixas = [cv2.boundingRect(c) for c in contornos]
    contornos_ordenados, _ = zip(*sorted(zip(contornos, caixas), key=lambda b: b[1][1]))
    return list(contornos_ordenados)


# =============================================================================
# 2. LÓGICA DE VISÃO COMPUTACIONAL (BACK-END OMR ROBUSTO)
# =============================================================================


def processar_imagem_opencv(imagem_pil, gabarito_oficial):
    try:
        # ETAPA 1: Preparação
        img = np.array(imagem_pil)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        h_orig, w_orig = img.shape[:2]
        largura_img = 700
        proporcao = largura_img / float(w_orig)
        altura_img = int(h_orig * proporcao)

        img = cv2.resize(img, (largura_img, altura_img))
        img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # ETAPA 2: Marcadores Fiduciários
        img_desfoque = cv2.GaussianBlur(img_cinza, (5, 5), 0)
        _, img_bin_marcadores = cv2.threshold(
            img_desfoque, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )
        contornos, _ = cv2.findContours(
            img_bin_marcadores, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        marcadores_validos = []
        for c in contornos:
            area = cv2.contourArea(c)
            if 50 < area < 15000:
                x, y, w, h = cv2.boundingRect(c)
                if 0.7 <= float(w) / h <= 1.3:
                    if (area / float(w * h)) > 0.7:
                        marcadores_validos.append((area, c))

        marcadores_validos.sort(key=lambda x: x[0], reverse=True)
        quatro_maiores = [item[1] for item in marcadores_validos[:4]]

        if len(quatro_maiores) < 4:
            return {
                "sucesso": False,
                "mensagem": "Erro: Os 4 cantos pretos não foram localizados.",
            }

        # ETAPA 3: Alinhamento de Perspectiva
        centros = []
        for c in quatro_maiores:
            M = cv2.moments(c)
            if M["m00"] != 0:
                centros.append([int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])])

        pontos_papel = ordenar_pontos(np.array(centros))
        pontos_destino = np.float32(
            [[0, 0], [largura_img, 0], [0, altura_img], [largura_img, altura_img]]
        )
        matriz = cv2.getPerspectiveTransform(pontos_papel, pontos_destino)
        img_alinhada = cv2.warpPerspective(img, matriz, (largura_img, altura_img))

        # ETAPA 4: Binarização Global para Leitura
        img_alinhada_cinza = cv2.cvtColor(img_alinhada, cv2.COLOR_BGR2GRAY)
        img_alinhada_suave = cv2.GaussianBlur(img_alinhada_cinza, (5, 5), 0)
        _, img_binaria = cv2.threshold(
            img_alinhada_suave, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )

        # Remove cabeçalho e rodapé grosseiramente para focar na grade
        img_grade_limpa = img_binaria[40 : altura_img - 20, 20 : largura_img - 20]
        img_alinhada_debug = img_alinhada[
            40 : altura_img - 20, 20 : largura_img - 20
        ].copy()

        # ETAPA 5: Divisão em Macro-Colunas
        qtd_questoes = len(gabarito_oficial)
        max_linhas_coluna = 25
        n_colunas = math.ceil(qtd_questoes / max_linhas_coluna)
        if n_colunas < 1:
            n_colunas = 1

        largura_coluna = img_grade_limpa.shape[1] // n_colunas

        mapa_letras = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
        nota = 0
        detalhes_correcao = []
        questao_atual_idx = 0

        # Iteração sobre cada coluna da página
        for i_col in range(n_colunas):
            x_inicio = i_col * largura_coluna
            x_fim = (i_col + 1) * largura_coluna
            if i_col == n_colunas - 1:
                x_fim = img_grade_limpa.shape[1]  # Garante pegar o resto

            coluna_img = img_grade_limpa[:, x_inicio:x_fim]

            # ETAPA 6: Encontrar as Bolinhas na Coluna (Busca Ativa de Contornos)
            contornos_coluna, _ = cv2.findContours(
                coluna_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            bolinhas_validas = []
            for c in contornos_coluna:
                x, y, w, h = cv2.boundingRect(c)
                aspect_ratio = w / float(h)

                # Filtro: A forma deve ser aproximadamente um quadrado/círculo com tamanho razoável
                if 12 <= w <= 50 and 12 <= h <= 50 and 0.7 <= aspect_ratio <= 1.3:
                    bolinhas_validas.append(c)

            # Ordena todas as bolinhas da coluna de cima para baixo
            try:
                bolinhas_validas = ordenar_contornos_cima_baixo(bolinhas_validas)
            except ValueError:
                return {
                    "sucesso": False,
                    "mensagem": f"Erro de leitura: Não foi possível identificar as alternativas na coluna {i_col+1}. O papel pode estar rasurado ou a foto sem nitidez.",
                }

            # Agrupa as bolinhas de 5 em 5 (cada grupo é uma questão)
            for q in range(0, len(bolinhas_validas), 5):
                if questao_atual_idx >= qtd_questoes:
                    break

                linha_contornos = bolinhas_validas[q : q + 5]

                # Se o algoritmo encontrou menos de 5 alternativas, pula para evitar quebra
                if len(linha_contornos) != 5:
                    detalhes_correcao.append(
                        f"Q{questao_atual_idx+1}: Erro de captura - alternativas ilegíveis."
                    )
                    questao_atual_idx += 1
                    continue

                # Ordena a questão da esquerda para a direita (A, B, C, D, E)
                linha_contornos = ordenar_contornos_esquerda_direita(linha_contornos)

                letra_gabarito = gabarito_oficial[questao_atual_idx]
                pixels_marcados = []

                # Conta a tinta de cada alternativa
                for j, c in enumerate(linha_contornos):
                    # Cria uma máscara vazia do tamanho da coluna
                    mask = np.zeros(coluna_img.shape, dtype="uint8")
                    cv2.drawContours(
                        mask, [c], -1, 255, -1
                    )  # Pinta a bolinha de branco na máscara

                    # Faz um AND bit a bit (Avalia a tinta apenas dentro do círculo exato da bolinha)
                    mask = cv2.bitwise_and(coluna_img, coluna_img, mask=mask)
                    total_pixels = cv2.countNonZero(mask)
                    pixels_marcados.append(total_pixels)

                    # Desenha retângulos verdes no debug para você ver onde o robô leu
                    bx, by, bw, bh = cv2.boundingRect(c)
                    cv2.rectangle(
                        img_alinhada_debug,
                        (x_inicio + bx, by),
                        (x_inicio + bx + bw, by + bh),
                        (0, 255, 0),
                        2,
                    )

                max_pixels = max(pixels_marcados)
                # Para ser considerada preenchida, a marcação deve cobrir boa parte do círculo
                if max_pixels < 50:
                    detalhes_correcao.append(
                        f"Q{questao_atual_idx+1}: Incorreta (Em branco, correta era {letra_gabarito})"
                    )
                else:
                    indice_marcado = pixels_marcados.index(max_pixels)
                    letra_aluno = mapa_letras[indice_marcado]

                    if letra_aluno == letra_gabarito:
                        nota += 1
                        detalhes_correcao.append(
                            f"Q{questao_atual_idx+1}: Correta (Marcou {letra_aluno})"
                        )
                    else:
                        detalhes_correcao.append(
                            f"Q{questao_atual_idx+1}: Incorreta (Marcou {letra_aluno}, correta era {letra_gabarito})"
                        )

                questao_atual_idx += 1

        return {
            "sucesso": True,
            "nota": nota,
            "total": qtd_questoes,
            "detalhes": "\n".join(detalhes_correcao),
            "img_alinhada": cv2.cvtColor(img_alinhada_debug, cv2.COLOR_BGR2RGB),
            "img_grade": img_grade_limpa,
        }

    except Exception as e:
        return {
            "sucesso": False,
            "mensagem": f"Erro técnico no processamento: {str(e)}",
        }


# =============================================================================
# 3. GERAÇÃO DE GABARITO (REPORTLAB) - ATUALIZADO PARA LINHAS MAIS GROSSAS
# =============================================================================


def gerar_gabarito_pdf(qtd_questoes):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4
    margem_externa = 30

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(
        largura / 2, altura - 30, "Gabarito Padrão - Correção Automática"
    )

    c.setFont("Helvetica", 11)
    c.drawString(
        margem_externa,
        altura - 60,
        "Nome: ___________________________________________________________",
    )
    c.drawString(largura - margem_externa - 130, altura - 60, "Data: ___/___/20__")

    margem_sup_marcadores = 90
    tamanho_marcador = 25
    c.setFillColor(colors.black)

    c.rect(
        margem_externa,
        altura - margem_sup_marcadores - tamanho_marcador,
        tamanho_marcador,
        tamanho_marcador,
        fill=1,
    )
    c.rect(
        largura - margem_externa - tamanho_marcador,
        altura - margem_sup_marcadores - tamanho_marcador,
        tamanho_marcador,
        tamanho_marcador,
        fill=1,
    )
    c.rect(margem_externa, margem_externa, tamanho_marcador, tamanho_marcador, fill=1)
    c.rect(
        largura - margem_externa - tamanho_marcador,
        margem_externa,
        tamanho_marcador,
        tamanho_marcador,
        fill=1,
    )

    max_linhas_coluna = 25
    n_colunas = math.ceil(qtd_questoes / max_linhas_coluna)
    if n_colunas < 1:
        n_colunas = 1

    largura_util = largura - 2 * margem_externa
    largura_coluna = largura_util / n_colunas
    topo_grade = altura - margem_sup_marcadores - 50
    base_grade = margem_externa + 20
    altura_util = topo_grade - base_grade
    altura_linha = altura_util / max_linhas_coluna
    alternativas = ["A", "B", "C", "D", "E"]

    # ATENÇÃO AQUI: Linhas mais grossas facilitam a identificação dos círculos pela câmera
    c.setLineWidth(1.5)

    for coluna_idx in range(n_colunas):
        x_coluna = margem_externa + coluna_idx * largura_coluna
        espaco_numero = 30
        espaco_bolinha = largura_coluna - espaco_numero - 10
        passo_bolinha = espaco_bolinha / len(alternativas)
        raio_bolinha = min(10, passo_bolinha * 0.3)

        for linha_idx in range(max_linhas_coluna):
            questao_idx = coluna_idx * max_linhas_coluna + linha_idx
            if questao_idx >= qtd_questoes:
                break

            y_centro = topo_grade - linha_idx * altura_linha - altura_linha / 2
            c.setFont("Helvetica", 10)
            c.drawString(x_coluna + 2, y_centro - 4, f"{questao_idx + 1:02d}.")

            for alt_idx, letra in enumerate(alternativas):
                x_centro = (
                    x_coluna
                    + espaco_numero
                    + passo_bolinha * alt_idx
                    + passo_bolinha / 2
                )

                c.circle(x_centro, y_centro, raio_bolinha, stroke=1, fill=0)
                c.setFont("Helvetica", 8)
                c.drawCentredString(x_centro, y_centro - 3, letra)

    c.save()
    buffer.seek(0)
    return buffer


# =============================================================================
# 4. INTERFACE DO USUÁRIO (FRONT-END STREAMLIT)
# =============================================================================

st.title("🎯 Corretor Automático de Gabaritos")
st.markdown(
    "Utilize a câmera do celular ou envie uma foto para corrigir provas instantaneamente."
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
        max_value=100,
        value=st.session_state.corretor_qtd_questoes,
        key="input_corretor_qtd",
    )

    gabarito_input = st.text_input(
        "Gabarito Oficial (Ex: ABCDE)",
        max_chars=st.session_state.corretor_qtd_questoes,
        key="input_corretor_gabarito",
    ).upper()

    if st.button("Salvar Gabarito", type="primary", key="btn_salvar_gabarito"):
        gabarito_limpo = "".join([c for c in gabarito_input if c in "ABCDE"])

        if len(gabarito_limpo) == st.session_state.corretor_qtd_questoes:
            st.session_state.corretor_gabarito_salvo = list(gabarito_limpo)
            st.success("Gabarito salvo no sistema!")
        else:
            st.error(
                f"Erro: O gabarito exige exatamente {st.session_state.corretor_qtd_questoes} alternativas válidas."
            )

    if st.session_state.corretor_gabarito_salvo:
        st.info(f"**Ativo:** {' - '.join(st.session_state.corretor_gabarito_salvo)}")
        if st.button("Resetar Memória", key="btn_reset_gabarito"):
            st.session_state.corretor_gabarito_salvo = []
            st.rerun()

    st.markdown("---")
    st.subheader("2. Gerar Folha Padrão")

    # ATENÇÃO: Se for testar, DEVE imprimir ou gerar um NOVO PDF após essa atualização.
    # O novo PDF tem linhas mais grossas nos círculos para o OpenCV detectar corretamente.
    pdf_buffer = gerar_gabarito_pdf(st.session_state.corretor_qtd_questoes)

    st.download_button(
        label="📄 Baixar Novo PDF do Gabarito",
        data=pdf_buffer,
        file_name=f"gabarito_oficial_{st.session_state.corretor_qtd_questoes}_questoes.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True,
    )

with col_captura:
    st.subheader("2. Correção")

    if not st.session_state.corretor_gabarito_salvo:
        st.warning(
            "Gere o gabarito oficial na coluna de configuração antes de prosseguir."
        )
    else:
        metodo_entrada = st.radio(
            "Método de Entrada:", ["Câmera", "Arquivo"], horizontal=True
        )

        imagem_carregada = None
        if metodo_entrada == "Câmera":
            imagem_carregada = st.camera_input(
                "Alinhe os 4 cantos na tela", key="camera_corretor"
            )
        else:
            imagem_carregada = st.file_uploader(
                "Upload da prova (.jpg/.png)", type=["jpg", "png"], key="upload"
            )

        if imagem_carregada is not None:
            if st.button(
                "Executar Correção da Prova", type="primary", use_container_width=True
            ):
                with st.spinner("Extraindo coordenadas dos contornos..."):
                    img = Image.open(imagem_carregada)
                    resultado = processar_imagem_opencv(
                        img, st.session_state.corretor_gabarito_salvo
                    )

                    if resultado["sucesso"]:
                        st.success("Operação concluída com sucesso!")
                        st.metric(
                            label="Nota Calculada",
                            value=f"{resultado['nota']} / {resultado['total']}",
                        )

                        with st.expander(
                            "Expandir Log de Correção Analítico", expanded=True
                        ):
                            st.text(resultado["detalhes"])

                        st.markdown("### Auditoria Visual (Contour Mapping)")
                        col_debug1, col_debug2 = st.columns(2)

                        with col_debug1:
                            st.markdown("**Bolinhas Mapeadas (Verde)**")
                            st.image(
                                resultado["img_alinhada"], use_container_width=True
                            )
                        with col_debug2:
                            st.markdown("**Visão Binária Global**")
                            st.image(
                                resultado["img_grade"],
                                use_container_width=True,
                                clamp=True,
                            )
                    else:
                        st.error(resultado["mensagem"])
