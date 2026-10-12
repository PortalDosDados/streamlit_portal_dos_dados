"""Funções utilitárias de UI e estilos compartilhados para a aplicação Streamlit."""

from pathlib import Path
import streamlit as st

# Diretório raiz do projeto (onde está o Dione_Nascimento.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_project_root() -> Path:
    """Retorna o caminho raiz absoluto do projeto."""
    return PROJECT_ROOT


def get_asset_path(relative_path: str) -> str:
    """Retorna o caminho absoluto para um arquivo dentro de assets."""
    clean_path = relative_path.replace("assets/", "").replace("./assets/", "")
    asset_file = PROJECT_ROOT / "assets" / clean_path
    if asset_file.exists():
        return str(asset_file)
    return str(PROJECT_ROOT / relative_path)


def load_css(file_path: str = "style.css"):
    """
    Lê o arquivo CSS local com suporte a caminho absoluto e UTF-8,
    injetando os estilos na aplicação Streamlit.
    """
    css_file = Path(file_path)
    if not css_file.is_absolute():
        css_file = PROJECT_ROOT / file_path

    try:
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Erro: O arquivo de estilos '{css_file}' não foi encontrado.")


def render_metric_card(title: str, value: str, subtitle: str = "", border_color: str = "#0A66C2"):
    """
    Renderiza um card de KPI customizado com borda lateral colorida e estilo responsivo.
    """
    sub_html = f"<div class='metric-card-subtitle'>{subtitle}</div>" if subtitle else ""
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: {border_color};">
            <div class="metric-card-title">{title}</div>
            <div class="metric-card-value">{value}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, description: str = "", icon_asset: str = None, icon_width: int = 140):
    """
    Renderiza o cabeçalho padronizado da página com ícone opcional e descrição.
    """
    if icon_asset:
        icon_path = get_asset_path(icon_asset)
        if Path(icon_path).exists():
            st.image(icon_path, width=icon_width)

    st.title(title)
    if description:
        st.markdown(f"<div class='justificado'>{description}</div>", unsafe_allow_html=True)
    st.divider()


def render_footer(show_banner: bool = True):
    """
    Renderiza o rodapé padrão em todas as páginas do Portal dos Dados,
    incluindo banner temático e menção institucional.
    """
    st.divider()
    if show_banner:
        banner_path = get_asset_path("fundo.jpg")
        if Path(banner_path).exists():
            try:
                st.image(banner_path, use_container_width=True)
            except Exception:
                pass

    st.markdown(
        """
        <div class="portal-footer">
            <b>Portal dos Dados</b> • Conectando Engenharia de Manutenção à Ciência de Dados
            <br>
            Desenvolvido por <b>Dione Nascimento</b>
        </div>
        """,
        unsafe_allow_html=True,
    )
