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
    """
    Ordena 4 pontos (X, Y) na ordem: Top-Left, Top-Right, Bottom-Left, Bottom-Right.
    Modificado para retornar float32, exigência da transformação de perspectiva do OpenCV.
    """
    pontos = pontos.reshape((4, 2))
    pontos_novos = np.zeros((4, 2), dtype=np.float32)

    # O ponto com a menor soma (x+y) é o canto superior esquerdo
    # O ponto com a maior soma é o canto inferior direito
    soma = pontos.sum(axis=1)
    pontos_novos[0] = pontos[np.argmin(soma)]
    pontos_novos[3] = pontos[np.argmax(soma)]

    # O ponto com a menor diferença (y-x) é o canto superior direito
    # O ponto com a maior diferença é o canto inferior esquerdo
    diferenca = np.diff(pontos, axis=1)
    pontos_novos[1] = pontos[np.argmin(diferenca)]
    pontos_novos[2] = pontos[np.argmax(diferenca)]

    return pontos_novos


# =============================================================================
# 2. LÓGICA DE VISÃO COMPUTACIONAL (BACK-END)
# =============================================================================


def processar_imagem_opencv(imagem_pil, gabarito_oficial):
    """
    Identifica os 4 quadrados pretos do gabarito, corrige a perspectiva através
    de seus centroides, extrai as marcações e calcula a nota final.
    """
    try:
        # ETAPA 1: Preparação de Imagem
        img = np.array(imagem_pil)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        largura_img, altura_img = 700, 700
        img = cv2.resize(img, (largura_img, altura_img))
        img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # ETAPA 2: Detecção dos Marcadores Fiduciários
        # Suaviza a imagem e aplica binarização invertida (escuro vira branco)
        img_desfoque = cv2.GaussianBlur(img_cinza, (5, 5), 0)
        _, img_bin_marcadores = cv2.threshold(
            img_desfoque, 120, 255, cv2.THRESH_BINARY_INV
        )

        contornos, _ = cv2.findContours(
            img_bin_marcadores, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        marcadores_validos = []

        for c in contornos:
            area = cv2.contourArea(c)
            # Filtro 1: Remove ruídos minúsculos e blocos gigantes
            if 100 < area < 5000:
                x, y, w, h = cv2.boundingRect(c)
                aspect_ratio = float(w) / h

                # Filtro 2: A forma deve ser quadrada (margem de tolerância 0.7 a 1.3)
                if 0.7 <= aspect_ratio <= 1.3:
                    solidez = area / float(w * h)

                    # Filtro 3: Deve ser sólido (não vazado)
                    if solidez > 0.7:
                        marcadores_validos.append((area, c))

        # Ordena os quadrados encontrados pela área (do maior para o menor)
        # e seleciona os 4 maiores. Isso previne falhas se a câmera pegar um
        # botão preto de camisa ou algo semelhante no fundo.
        marcadores_validos.sort(key=lambda x: x[0], reverse=True)
        quatro_maiores = [item[1] for item in marcadores_validos[:4]]

        if len(quatro_maiores) < 4:
            return {
                "sucesso": False,
                "mensagem": f"Erro: Foram encontrados apenas {len(quatro_maiores)} quadrados marcadores. Posicione a câmera de modo que os 4 cantos fiquem visíveis.",
            }

        # ETAPA 3: Cálculo dos Centroides e Alinhamento
        centros = []
        for c in quatro_maiores:
            M = cv2.moments(c)
            # Evita divisão por zero (segurança)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centros.append([cX, cY])

        pontos_papel = ordenar_pontos(np.array(centros))
        pontos_destino = np.float32(
            [[0, 0], [largura_img, 0], [0, altura_img], [largura_img, altura_img]]
        )

        # Mapeia a imagem ancorando os 4 centros dos quadrados nos 4 cantos da nova imagem
        matriz = cv2.getPerspectiveTransform(pontos_papel, pontos_destino)
        img_alinhada = cv2.warpPerspective(img, matriz, (largura_img, altura_img))

        # ETAPA 4: Binarização Adaptativa para Leitura da Tinta
        img_alinhada_cinza = cv2.cvtColor(img_alinhada, cv2.COLOR_BGR2GRAY)
        img_alinhada_suave = cv2.GaussianBlur(img_alinhada_cinza, (5, 5), 0)

        img_binaria = cv2.adaptiveThreshold(
            img_alinhada_suave,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2,
        )

        # ETAPA 4.1: Recorte da Região de Interesse (ROI)
        # Os novos cortes são menores pois a imagem alinhada já começa no centro dos marcadores
        corte_topo = 40  # Remove cabeçalho e instrução
        corte_base = 20
        corte_esq = (
            55  # Remove as numerações (01., 02.) para evitar leitura de tinta falsa
        )
        corte_dir = 20

        img_grade_limpa = img_binaria[
            corte_topo : altura_img - corte_base, corte_esq : largura_img - corte_dir
        ]

        # ETAPA 5: Dimensionamento Preciso para grid de colunas
        qtd_questoes = len(gabarito_oficial)
        qtd_alternativas = 5
        max_linhas_coluna = 25

        n_colunas = math.ceil(qtd_questoes / max_linhas_coluna)
        if n_colunas < 1:
            n_colunas = 1

        # A altura precisa ser múltipla de 25 para dividir em 25 linhas exatas.
        altura_ideal = (
            img_grade_limpa.shape[0] // max_linhas_coluna
        ) * max_linhas_coluna

        # Cada coluna deve ser um múltiplo de 5 para que as 5 alternativas sejam igualmente divididas.
        largura_por_coluna = img_grade_limpa.shape[1] // n_colunas
        largura_por_coluna = (largura_por_coluna // qtd_alternativas) * qtd_alternativas
        largura_ideal = largura_por_coluna * n_colunas

        img_grade_limpa = cv2.resize(img_grade_limpa, (largura_ideal, altura_ideal))

        # ETAPA 6: Divisão da Grade em colunas e linhas
        colunas = np.hsplit(img_grade_limpa, n_colunas)
        caixas_alternativas = []

        for coluna in colunas:
            # Descarrega 20% da margem esquerda da coluna para apagar números como "26.".
            margem_esquerda = int(coluna.shape[1] * 0.2)
            coluna_sem_numeros = coluna[:, margem_esquerda:]

            # Cada coluna corresponde a até 25 questões; dividimos em 25 linhas exatas.
            linhas_coluna = np.vsplit(coluna_sem_numeros, max_linhas_coluna)
            for linha in linhas_coluna:
                # Dentro de cada linha, existem 5 alternativas.
                alternativas = np.hsplit(linha, qtd_alternativas)
                for caixa in alternativas:
                    caixas_alternativas.append(caixa)

        # ETAPA 7: Contagem de Pixels e Auditoria
        respostas_aluno_indices = []
        indice_caixa = 0

        area_caixa = (altura_ideal // qtd_questoes) * (
            largura_ideal // qtd_alternativas
        )
        limite_pixels = area_caixa * 0.15

        for i in range(qtd_questoes):
            pixels_por_alternativa = []
            for j in range(qtd_alternativas):
                total_pixels = cv2.countNonZero(caixas_alternativas[indice_caixa])
                pixels_por_alternativa.append(total_pixels)
                indice_caixa += 1

            max_pixels = max(pixels_por_alternativa)

            if max_pixels < limite_pixels:
                respostas_aluno_indices.append(-1)
            else:
                respostas_aluno_indices.append(pixels_por_alternativa.index(max_pixels))

        mapa_letras = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
        nota = 0
        detalhes_correcao = []

        for i in range(qtd_questoes):
            letra_gabarito = gabarito_oficial[i]

            if respostas_aluno_indices[i] == -1:
                detalhes_correcao.append(
                    f"Q{i+1}: Incorreta (Em branco, correta era {letra_gabarito})"
                )
                continue

            letra_aluno = mapa_letras[respostas_aluno_indices[i]]

            if letra_aluno == letra_gabarito:
                nota += 1
                detalhes_correcao.append(f"Q{i+1}: Correta (Marcou {letra_aluno})")
            else:
                detalhes_correcao.append(
                    f"Q{i+1}: Incorreta (Marcou {letra_aluno}, correta era {letra_gabarito})"
                )

        return {
            "sucesso": True,
            "nota": nota,
            "total": qtd_questoes,
            "detalhes": "\n".join(detalhes_correcao),
            "img_alinhada": cv2.cvtColor(img_alinhada, cv2.COLOR_BGR2RGB),
            "img_grade": img_grade_limpa,
        }

    except Exception as e:
        return {
            "sucesso": False,
            "mensagem": f"Erro técnico no processamento. Log: {str(e)}",
        }


# =============================================================================
# 3. GERAÇÃO DE GABARITO (REPORTLAB)
# =============================================================================


def gerar_gabarito_pdf(qtd_questoes):
    """
    Gera um arquivo PDF contendo um template de gabarito em uma única página A4.
    Os campos de identificação (Nome/Data) estão fora da área dos marcadores
    fiduciários para garantir que o OpenCV não capture a tinta da caneta do aluno.
    """
    buffer = io.BytesIO()

    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4
    margem_externa = 30

    # --- CABEÇALHO E IDENTIFICAÇÃO (AGORA FORA DA ZONA DE CAPTURA) ---
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(
        largura / 2, altura - 30, "Gabarito Padrão - Correção Automática"
    )

    c.setFont("Helvetica", 11)
    # Alinhado à margem esquerda
    c.drawString(
        margem_externa,
        altura - 60,
        "Nome: ___________________________________________________________",
    )
    # Alinhado à direita
    c.drawString(largura - margem_externa - 130, altura - 60, "Data: ___/___/20__")

    # --- MARCADORES FIDUCIÁRIOS (ÂNCORAS PARA O OPENCV) ---
    # Os marcadores superiores foram rebaixados (Y = 90) para ficar abaixo do cabeçalho
    margem_sup_marcadores = 90
    tamanho_marcador = 25
    c.setFillColor(colors.black)

    # Top-Left
    c.rect(
        margem_externa,
        altura - margem_sup_marcadores - tamanho_marcador,
        tamanho_marcador,
        tamanho_marcador,
        fill=1,
    )
    # Top-Right
    c.rect(
        largura - margem_externa - tamanho_marcador,
        altura - margem_sup_marcadores - tamanho_marcador,
        tamanho_marcador,
        tamanho_marcador,
        fill=1,
    )
    # Bottom-Left
    c.rect(margem_externa, margem_externa, tamanho_marcador, tamanho_marcador, fill=1)
    # Bottom-Right
    c.rect(
        largura - margem_externa - tamanho_marcador,
        margem_externa,
        tamanho_marcador,
        tamanho_marcador,
        fill=1,
    )

    # --- GRADE DE QUESTÕES ---
    max_linhas_coluna = 25
    n_colunas = math.ceil(qtd_questoes / max_linhas_coluna)
    if n_colunas < 1:
        n_colunas = 1

    largura_util = largura - 2 * margem_externa
    largura_coluna = largura_util / n_colunas

    # O topo da grade acompanha os marcadores rebaixados
    topo_grade = altura - margem_sup_marcadores - 50
    base_grade = margem_externa + 20
    altura_util = topo_grade - base_grade
    altura_linha = altura_util / max_linhas_coluna

    alternativas = ["A", "B", "C", "D", "E"]

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
# 4. INTERFACE DO USUÁRIO (FRONT-END STREAMLIT) - MOVIDO PARA BAIXO
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
    st.markdown(
        "Imprima este arquivo e utilize-o para aplicar a prova. Ele contém marcações para garantir a leitura precisa."
    )

    # Função agora é reconhecida pois foi declarada antes de ser chamada!
    pdf_buffer = gerar_gabarito_pdf(st.session_state.corretor_qtd_questoes)

    st.download_button(
        label="📄 Baixar PDF do Gabarito",
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
            "Método de Entrada da Imagem:",
            ["Câmera", "Arquivo"],
            horizontal=True,
            key="radio_metodo_captura",
        )

        imagem_carregada = None

        if metodo_entrada == "Câmera":
            imagem_carregada = st.camera_input(
                "Alinhe os 4 cantos do gabarito na tela", key="camera_corretor"
            )
        else:
            imagem_carregada = st.file_uploader(
                "Realize o upload da prova (.jpg/.png)",
                type=["jpg", "jpeg", "png"],
                key="upload_corretor",
            )

        if imagem_carregada is not None:
            if st.button(
                "Executar Correção da Prova",
                type="primary",
                use_container_width=True,
                key="btn_processar_correcao",
            ):
                with st.spinner("Processando a imagem e extraindo respostas..."):
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

                        st.markdown("### Auditoria Visual do Algoritmo")
                        col_debug1, col_debug2 = st.columns(2)
                        with col_debug1:
                            st.image(
                                resultado["img_alinhada"], use_container_width=True
                            )
                        with col_debug2:
                            st.image(
                                resultado["img_grade"],
                                use_container_width=True,
                                clamp=True,
                            )
                    else:
                        st.error(resultado["mensagem"])
