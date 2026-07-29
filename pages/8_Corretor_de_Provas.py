import streamlit as st
import cv2
import numpy as np
from PIL import Image


# ---------------------------------------------------------
# LÓGICA DE VISÃO COMPUTACIONAL (BACK-END)
# ---------------------------------------------------------
def processar_imagem_opencv(imagem_pil, gabarito_oficial):
    """
    Função que processa a imagem da prova e compara com o gabarito.
    """
    # Converte a imagem capturada na tela (PIL) para o formato numérico do OpenCV (NumPy)
    img_array = np.array(imagem_pil)

    # Converte as cores de RGB (web) para BGR (padrão de leitura do OpenCV)
    img_cv2 = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # =====================================================
    # O ALGORITMO DE CORREÇÃO DO OPENCV ENTRARÁ AQUI
    # =====================================================

    # Retorno temporário para garantirmos que a interface funciona
    return {
        "sucesso": True,
        "nota": 0,
        "total": len(gabarito_oficial),
        "detalhes": "A lógica do OpenCV será integrada na próxima etapa.",
    }


# ---------------------------------------------------------
# INTERFACE DO USUÁRIO (FRONT-END)
# ---------------------------------------------------------

st.title("🎯 Corretor Automático de Gabaritos")
st.markdown(
    "Utilize a câmera do celular ou envie uma foto para corrigir provas instantaneamente."
)

# Inicializa as variáveis na memória com prefixo 'corretor_' para evitar conflitos com outras páginas
if "corretor_gabarito_salvo" not in st.session_state:
    st.session_state.corretor_gabarito_salvo = []
if "corretor_qtd_questoes" not in st.session_state:
    st.session_state.corretor_qtd_questoes = 10

# Dividimos a tela em duas colunas para melhor aproveitamento do espaço
col_config, col_captura = st.columns([1, 2])

# --- COLUNA 1: CONFIGURAÇÃO DO GABARITO ---
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
        # Limpa qualquer caractere que não seja de A a E
        gabarito_limpo = "".join([c for c in gabarito_input if c in "ABCDE"])

        if len(gabarito_limpo) == st.session_state.corretor_qtd_questoes:
            st.session_state.corretor_gabarito_salvo = list(gabarito_limpo)
            st.success("Gabarito salvo!")
        else:
            st.error(
                f"Digite exatamente {st.session_state.corretor_qtd_questoes} letras."
            )

    # Mostra o gabarito salvo
    if st.session_state.corretor_gabarito_salvo:
        st.info(f"**Ativo:** {' - '.join(st.session_state.corretor_gabarito_salvo)}")
        if st.button("Resetar Gabarito", key="btn_reset_gabarito"):
            st.session_state.corretor_gabarito_salvo = []
            st.rerun()

# --- COLUNA 2: CAPTURA E CORREÇÃO ---
with col_captura:
    st.subheader("2. Correção")

    if not st.session_state.corretor_gabarito_salvo:
        st.warning("Salve o gabarito na coluna ao lado para iniciar.")
    else:
        metodo_entrada = st.radio(
            "Método de Captura:",
            ["Câmera", "Arquivo"],
            horizontal=True,
            key="radio_metodo_captura",
        )

        imagem_carregada = None

        if metodo_entrada == "Câmera":
            imagem_carregada = st.camera_input(
                "Posicione o gabarito na tela", key="camera_corretor"
            )
        else:
            imagem_carregada = st.file_uploader(
                "Envie a foto", type=["jpg", "jpeg", "png"], key="upload_corretor"
            )

        if imagem_carregada is not None:
            if st.button(
                "Corrigir Prova",
                type="primary",
                use_container_width=True,
                key="btn_processar_correcao",
            ):
                with st.spinner("Processando imagem..."):
                    # Abre o arquivo de imagem carregado pelo usuário
                    img = Image.open(imagem_carregada)

                    # Chama a função principal de cálculo
                    resultado = processar_imagem_opencv(
                        img, st.session_state.corretor_gabarito_salvo
                    )

                    # Exibe o resultado final na interface
                    if resultado["sucesso"]:
                        st.success("Correção Finalizada!")
                        st.metric(
                            label="Nota Final",
                            value=f"{resultado['nota']} / {resultado['total']}",
                        )
                        with st.expander("Ver detalhes", expanded=True):
                            st.text(resultado["detalhes"])
                    else:
                        st.error(resultado["mensagem"])
