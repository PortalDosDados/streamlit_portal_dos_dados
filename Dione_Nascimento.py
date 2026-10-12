import streamlit as st
from utils.ui import load_css, get_asset_path, render_footer

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Portal dos Dados - Dione Nascimento",
    page_icon=get_asset_path("portal.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

# Carregamento dos estilos globais
load_css("style.css")

# --------------------------------------------------------------------------
# Seção: Header e Perfil Profissional
# --------------------------------------------------------------------------
with st.container():
    col_foto, col_bio = st.columns([1, 4], gap="medium")

    with col_foto:
        try:
            st.image(get_asset_path("minha_foto.png"), use_container_width=True)
        except Exception:
            st.warning("Imagem de perfil não disponível.")

    with col_bio:
        st.markdown(
            """
            <div class='justificado' style='padding-right: 10px;'>
                <p style='margin-top: 0;'>Olá! Sou <b>Dione Nascimento</b>, profissional com <b>15 anos de experiência em Manutenção Industrial</b>,
                especializado em <b>Gestão de Ativos</b> e <b>Análise de Dados</b>. Minha atuação combina metodologias
                de engenharia com soluções de Business Intelligence para transformar dados operacionais em decisões estratégicas.</p>
                <p>Minha trajetória iniciou no SENAI (como aprendiz e professor) e consolidou-se no <b>setor siderúrgico</b>,
                onde desenvolvo projetos de:</p>
                <ul>
                    <li><b>Confiabilidade de equipamentos</b>;</li>
                    <li><b>Digitalização da manutenção</b>;</li>
                    <li><b>Automação de indicadores (KPIs)</b>.</li>
                </ul>
                <p>Sou fundador do <b>Portal dos Dados</b>, uma iniciativa que conecta a Engenharia de Manutenção à Ciência de Dados,
                capacitando profissionais a eliminarem o 'achismo' através de dados reais.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --------------------------------------------------------------------------
# Seção: Banner e Proposta de Valor
# --------------------------------------------------------------------------
try:
    st.image(get_asset_path("fundo.jpg"), use_container_width=True)
except Exception:
    pass

st.markdown(
    """
    <div class='justificado'>
        <p><b>PORTAL DOS DADOS</b> é um hub de conhecimento focado em produtividade técnica.
        Aqui, a teoria encontra a prática do chão de fábrica.</p>
        <p><b>Pilares de Conteúdo:</b></p>
        <ul>
            <li>🐍 <b>Python & Automação:</b> Scripts para eliminar tarefas repetitivas.</li>
            <li>📊 <b>Power BI & Analytics:</b> Dashboards para gestão à vista.</li>
            <li>📱 <b>Power Platform:</b> Apps (Power Apps) e Fluxos (Automate) corporativos.</li>
            <li>🗄️ <b>Engenharia de Dados:</b> SQL e estruturação de bancos industriais.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Seção: Rodapé e Redes Sociais (Call to Action)
# --------------------------------------------------------------------------
st.markdown("### 🤝 Vamos nos conectar?")
st.markdown("Explore meus projetos ou entre em contato profissionalmente:")

col_btn1, col_btn2, col_btn3, _ = st.columns([1, 1, 1, 2], gap="small")

# Botão: LinkedIn
with col_btn1:
    st.markdown(
        """
        <a href='https://www.linkedin.com/in/dione-nascimento-37287a233/' target='_blank' style='text-decoration: none;'>
            <button class='btn-linkedin'>
                <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>
                    <path d='M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z'/>
                </svg>
                <span>LinkedIn</span>
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

# Botão: YouTube
with col_btn2:
    st.markdown(
        """
        <a href='https://www.youtube.com/@Portal_dos_Dados' target='_blank' style='text-decoration: none;'>
            <button class='btn-youtube'>
                <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>
                    <path d='M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z'/>
                </svg>
                <span>YouTube</span>
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

# Botão: GitHub
with col_btn3:
    st.markdown(
        """
        <a href='https://github.com/PortalDosDados' target='_blank' style='text-decoration: none;'>
            <button class='btn-github'>
                <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>
                    <path d='M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z'/>
                </svg>
                <span>GitHub</span>
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

render_footer(show_banner=False)
