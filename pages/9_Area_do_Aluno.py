import streamlit as st
from datetime import datetime
import smtplib
from email.message import EmailMessage

# ==========================================
# 1. Configuração Visual (Injeção de CSS)
# ==========================================
st.set_page_config(page_title="Portal de Atividades", layout="centered")

st.markdown(
    """
<style>
    /* Estilo idêntico à imagem de referência */
    .card-container {
        background-color: #f1f3f4;
        border-left: 6px solid #005088;
        padding: 15px 20px;
        margin-top: 15px;
        margin-bottom: 5px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .card-title {
        color: #005088;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .card-desc {
        color: #555555;
        font-size: 14px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. Banco de Dados Estruturado
# ==========================================
# Estrutura atualizada: cada chave principal é o Título do Card
banco_provas = {
    "Simbologia AWS - Exercício 01": {
        "descricao": "Avaliação técnica sobre os fundamentos de soldagem e interpretação de símbolos básicos.",
        "questoes": [
            {
                "eixo": "Geometria de Juntas",
                "contexto": "Elementos Básicos",
                "comando": "O que define o 'Ângulo de Bisel'?",
                "options": [
                    "O ângulo total formado entre as duas peças a serem soldadas.",
                    "O ângulo preparado na borda de uma única peça.",
                    "A distância entre as duas peças na raiz da junta.",
                    "A face plana não chanfrada na raiz da junta.",
                ],
                "correct": 1,
                "just": "O ângulo de bisel refere-se à inclinação usinada ou cortada na borda de apenas uma das chapas.",
            }
            # Adicione as demais questões de AWS aqui
        ],
    },
    "Metrologia - Exercício 01": {
        "descricao": "Avaliação técnica sobre os fundamentos e conversões de sistemas de medidas.",
        "questoes": [
            {
                "eixo": "Fundamentos",
                "contexto": "Calibração",
                "comando": "Qual é o principal objetivo da calibração de um instrumento?",
                "options": [
                    "Ajustar o instrumento para erro zero.",
                    "Estabelecer a relação com um padrão de referência.",
                    "Consertar peças internas desgastadas.",
                    "Aumentar o tempo de vida útil do equipamento.",
                ],
                "correct": 1,
                "just": "A calibração não conserta o erro, apenas estabelece o desvio em relação a um padrão conhecido.",
            }
            # Adicione as demais questões de Metrologia aqui
        ],
    },
    "Desenho Técnico - Exercício 01": {
        "descricao": "Leitura e interpretação de vistas ortográficas e tipos de linhas mecânicas.",
        "questoes": [
            {
                "eixo": "Leitura e Interpretação",
                "contexto": "Tipos de Linhas",
                "comando": "O que indica uma linha tracejada em um desenho técnico mecânico?",
                "options": [
                    "Arestas e contornos visíveis.",
                    "Linhas de centro e simetria.",
                    "Arestas e contornos não visíveis (ocultos).",
                    "Indicação de corte na peça.",
                ],
                "correct": 2,
                "just": "Linhas tracejadas representam arestas e contornos que não podem ser vistos diretamente na vista atual do observador.",
            }
            # Adicione as demais questões de Desenho Técnico aqui
        ],
    },
}

# ==========================================
# 3. Inicialização de Variáveis de Estado
# ==========================================
if "etapa" not in st.session_state:
    st.session_state.etapa = "menu"  # Alterado para iniciar no novo Menu de Cards
if "disciplina_atual" not in st.session_state:
    st.session_state.disciplina_atual = None
if "questao_atual" not in st.session_state:
    st.session_state.questao_atual = 0
if "respostas_usuario" not in st.session_state:
    st.session_state.respostas_usuario = []
if "nome_aluno" not in st.session_state:
    st.session_state.nome_aluno = ""


# Função auxiliar para resetar o teste ao trocar ou iniciar disciplina
def preparar_teste(titulo_disciplina):
    st.session_state.disciplina_atual = titulo_disciplina
    st.session_state.etapa = "identificacao"
    st.session_state.questao_atual = 0
    st.session_state.respostas_usuario = [None] * len(
        banco_provas[titulo_disciplina]["questoes"]
    )
    st.session_state.nome_aluno = ""


# ==========================================
# TELA 0: Portal de Atividades (Dashboard)
# ==========================================
if st.session_state.etapa == "menu":
    st.markdown(
        "<h2 style='text-align: center; color: #555;'>Portal de Atividades - Prof. Dione Nascimento</h2>",
        unsafe_allow_html=True,
    )
    st.write("")  # Espaçamento

    # Loop para renderizar os cards visualmente baseados no dicionário
    for titulo, dados in banco_provas.items():
        st.markdown(
            f"""
        <div class="card-container">
            <div class="card-title">{titulo}</div>
            <div class="card-desc">{dados['descricao']}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # O botão nativo fica anexado logo abaixo do card para processar o clique no Python
        if st.button(
            f"Iniciar {titulo}", key=f"btn_{titulo}", use_container_width=True
        ):
            preparar_teste(titulo)
            st.rerun()

# ==========================================
# TELA 1: Identificação do Aluno
# ==========================================
elif st.session_state.etapa == "identificacao":
    if st.button("⬅ Voltar ao Menu Principal"):
        st.session_state.etapa = "menu"
        st.rerun()

    st.divider()
    st.subheader(f"Módulo Selecionado: {st.session_state.disciplina_atual}")
    nome_input = st.text_input(
        "Nome Completo:",
        placeholder="Digite seu nome completo aqui para o relatório...",
    )

    if st.button("Avançar para a Prova", type="primary"):
        if nome_input.strip() == "":
            st.warning("O preenchimento do nome é obrigatório.")
        else:
            st.session_state.nome_aluno = nome_input
            st.session_state.etapa = "quiz"
            st.rerun()

# ==========================================
# TELA 2: Navegação das Questões
# ==========================================
elif st.session_state.etapa == "quiz":
    quiz_data = banco_provas[st.session_state.disciplina_atual]["questoes"]
    idx = st.session_state.questao_atual
    q = quiz_data[idx]

    st.markdown(
        f"<span style='color:#005088;font-size:14px;font-weight:bold;'>[{q['eixo']}] Questão {idx + 1} de {len(quiz_data)}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(f"*{q['contexto']}*")
    st.markdown(f"**{q['comando']}**")

    resposta_selecionada = st.radio(
        "Selecione uma alternativa:",
        options=q["options"],
        index=None,
        label_visibility="collapsed",
    )

    st.divider()

    if st.button(
        "Confirmar e Avançar" if idx < len(quiz_data) - 1 else "Finalizar Exercício"
    ):
        if resposta_selecionada is None:
            st.warning("Selecione uma alternativa antes de avançar.")
        else:
            indice_resposta = q["options"].index(resposta_selecionada)
            st.session_state.respostas_usuario[idx] = indice_resposta

            if idx < len(quiz_data) - 1:
                st.session_state.questao_atual += 1
            else:
                st.session_state.etapa = "resultado"
            st.rerun()

# ==========================================
# TELA 3: Resultados e Envio de E-mail
# ==========================================
elif st.session_state.etapa == "resultado":
    st.header("Relatório do Exercício de Fixação")
    quiz_data = banco_provas[st.session_state.disciplina_atual]["questoes"]

    acertos = 0
    for i, q in enumerate(quiz_data):
        if st.session_state.respostas_usuario[i] == q["correct"]:
            acertos += 1

    total = len(quiz_data)
    pct = (acertos / total) * 100
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    st.success(
        f"**Aluno:** {st.session_state.nome_aluno} | **Disciplina:** {st.session_state.disciplina_atual} | **Data:** {data_atual}"
    )
    st.markdown(f"### Acertos: {acertos} / {total} ({pct:.1f}%)")

    if pct >= 80:
        st.info("Excelente retenção de conhecimento!")
    elif pct >= 60:
        st.warning("Bom trabalho. Revise as justificativas das questões que errou.")
    else:
        st.error("Atenção: Revise os conceitos fundamentais desta disciplina.")

    st.divider()
    st.subheader("Revisão das Questões")

    for i, q in enumerate(quiz_data):
        resposta_usuario = st.session_state.respostas_usuario[i]
        esta_correto = resposta_usuario == q["correct"]

        letra_usuario = (
            chr(65 + resposta_usuario) if resposta_usuario is not None else "N/A"
        )
        letra_correta = chr(65 + q["correct"])
        cor_borda = "#10b981" if esta_correto else "#ef4444"

        st.markdown(
            f"""
        <div style="border-left: 5px solid {cor_borda}; padding: 10px; background-color: #f9f9f9; margin-bottom: 10px;">
            <strong>Questão {i + 1} ({q['eixo']})</strong><br>
            <em>Sua resposta: {letra_usuario} | Resposta correta: {letra_correta}</em><br>
            <strong>Justificativa Técnica:</strong> {q['just']}
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Enviar Exercício ao Professor", type="primary", use_container_width=True
        ):
            with st.spinner("Conectando ao servidor..."):
                try:
                    email_remetente = st.secrets["EMAIL_REMETENTE"]
                    email_senha = st.secrets["EMAIL_SENHA"]
                    email_destino = st.secrets["EMAIL_DESTINO"]

                    msg = EmailMessage()
                    msg["Subject"] = (
                        f"Resultado: {st.session_state.disciplina_atual} - {st.session_state.nome_aluno}"
                    )
                    msg["From"] = email_remetente
                    msg["To"] = email_destino

                    conteudo_email = f"""
Relatório de Exercício de Fixação

Aluno: {st.session_state.nome_aluno}
Módulo: {st.session_state.disciplina_atual}
Data: {data_atual}

Nota: {acertos} de {total} ({pct:.1f}%)
                    """
                    msg.set_content(conteudo_email)

                    servidor_smtp = "smtp.gmail.com"
                    porta = 587

                    with smtplib.SMTP(servidor_smtp, porta) as server:
                        server.starttls()
                        server.login(email_remetente, email_senha)
                        server.send_message(msg)

                    st.success("✅ E-mail enviado com sucesso!")

                except Exception as e:
                    st.error(f"❌ Ocorreu um erro técnico: {e}")

    with col2:
        if st.button("Voltar ao Menu Principal", use_container_width=True):
            st.session_state.etapa = "menu"
            st.rerun()
