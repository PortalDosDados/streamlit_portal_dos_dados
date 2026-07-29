import streamlit as st
import cv2
import numpy as np
from PIL import Image

# =============================================================================
# 1. FUNÇÕES AUXILIARES (GEOMETRIA)
# =============================================================================


def ordenar_pontos(pontos):
    """
    Ordena os 4 pontos do contorno do papel detectado pela câmera.
    A ordem (Top-Left, Top-Right, Bottom-Left, Bottom-Right) é necessária
    para que o cálculo de perspectiva não rotacione a imagem indevidamente.
    """
    pontos = pontos.reshape((4, 2))
    pontos_novos = np.zeros((4, 1, 2), np.int32)

    soma = pontos.sum(1)
    pontos_novos[0] = pontos[np.argmin(soma)]
    pontos_novos[3] = pontos[np.argmax(soma)]

    diferenca = np.diff(pontos, axis=1)
    pontos_novos[1] = pontos[np.argmin(diferenca)]
    pontos_novos[2] = pontos[np.argmax(diferenca)]

    return pontos_novos


# =============================================================================
# 2. LÓGICA DE VISÃO COMPUTACIONAL (BACK-END)
# =============================================================================


def processar_imagem_opencv(imagem_pil, gabarito_oficial):
    """
    Recebe a imagem, identifica o papel, corrige iluminação, recorta as bolinhas e calcula a nota.
    """
    try:
        # ETAPA 1: Preparação de Imagem
        img = np.array(imagem_pil)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        largura_img, altura_img = 700, 700
        img = cv2.resize(img, (largura_img, altura_img))

        img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_desfoque = cv2.GaussianBlur(img_cinza, (5, 5), 1)
        img_bordas = cv2.Canny(img_desfoque, 10, 50)

        # ETAPA 2: Detecção do Papel
        contornos, _ = cv2.findContours(
            img_bordas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        maior_contorno = np.array([])
        maior_area = 0

        for c in contornos:
            area = cv2.contourArea(c)
            if area > 5000:
                perimetro = cv2.arcLength(c, True)
                poligono = cv2.approxPolyDP(c, 0.02 * perimetro, True)
                if len(poligono) == 4 and area > maior_area:
                    maior_contorno = poligono
                    maior_area = area

        if maior_contorno.size == 0:
            return {
                "sucesso": False,
                "mensagem": "O contorno da prova não foi identificado.",
            }

        # ETAPA 3: Alinhamento e Perspectiva
        pontos_papel = ordenar_pontos(maior_contorno)
        pontos_destino = np.float32(
            [[0, 0], [largura_img, 0], [0, altura_img], [largura_img, altura_img]]
        )

        matriz = cv2.getPerspectiveTransform(np.float32(pontos_papel), pontos_destino)
        img_alinhada = cv2.warpPerspective(img, matriz, (largura_img, altura_img))

        # ETAPA 4: Binarização Adaptativa (Ignora Sombras)
        img_alinhada_cinza = cv2.cvtColor(img_alinhada, cv2.COLOR_BGR2GRAY)
        img_alinhada_suave = cv2.GaussianBlur(img_alinhada_cinza, (5, 5), 0)

        # Analisa blocos de 11x11 pixels para decidir o contraste, isolando a tinta da sombra
        img_binaria = cv2.adaptiveThreshold(
            img_alinhada_suave,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2,
        )

        # ETAPA 4.1: Recorte da Região de Interesse (ROI)
        # Arranca as margens para eliminar textos (Q01, A, B, C...) e evitar falsos positivos
        corte_topo = 70
        corte_base = 20
        corte_esq = 80
        corte_dir = 20

        img_grade_limpa = img_binaria[
            corte_topo : 700 - corte_base, corte_esq : 700 - corte_dir
        ]
        img_grade_limpa = cv2.resize(img_grade_limpa, (500, 500))

        # ETAPA 5: Divisão da Grade Matemática
        qtd_questoes = len(gabarito_oficial)
        qtd_alternativas = 5

        linhas = np.vsplit(img_grade_limpa, qtd_questoes)
        caixas_alternativas = []
        for linha in linhas:
            colunas = np.hsplit(linha, qtd_alternativas)
            for caixa in colunas:
                caixas_alternativas.append(caixa)

        # ETAPA 6: Contagem de Pixels e Decisão
        respostas_aluno_indices = []
        indice_caixa = 0

        for i in range(qtd_questoes):
            pixels_por_alternativa = []
            for j in range(qtd_alternativas):
                # Mede a densidade do preenchimento a caneta
                total_pixels = cv2.countNonZero(caixas_alternativas[indice_caixa])
                pixels_por_alternativa.append(total_pixels)
                indice_caixa += 1

            indice_marcado = pixels_por_alternativa.index(max(pixels_por_alternativa))
            respostas_aluno_indices.append(indice_marcado)

        # ETAPA 7: Auditoria e Resultado Final
        mapa_letras = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
        nota = 0
        detalhes_correcao = []

        for i in range(qtd_questoes):
            letra_aluno = mapa_letras[respostas_aluno_indices[i]]
            letra_gabarito = gabarito_oficial[i]

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
        }

    except Exception as e:
        return {
            "sucesso": False,
            "mensagem": f"Erro técnico no processamento da grade. Log: {str(e)}",
        }


# =============================================================================
# 3. INTERFACE DO USUÁRIO (FRONT-END STREAMLIT)
# =============================================================================

st.title("🎯 Corretor Automático de Gabaritos")
st.markdown(
    "Utilize a câmera do celular ou envie uma foto para corrigir provas instantaneamente."
)

# Variáveis isoladas com o prefixo 'corretor_' para evitar conflito com outras abas
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
                with st.spinner(
                    "Compilando algoritmo e analisando matriz de pixels..."
                ):

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
                    else:
                        st.error(resultado["mensagem"])
