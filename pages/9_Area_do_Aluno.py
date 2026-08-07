import streamlit as st
from datetime import datetime
import smtplib
from email.message import EmailMessage

# Configuração da página e título da disciplina
st.title("SENAI | Exercício de Fixação")
st.markdown("### Preparação para os Processos de Corte e Soldagem")
st.info(
    "**Atenção Turma:** Esta atividade não possui caráter de nota. O objetivo é testar os seus conhecimentos em Elementos de Chanfro e Simbologia AWS!"
)

st.divider()

# Banco de Dados do Quiz (Pode adicionar as demais questões aqui)
quiz_data = [
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
        "just": "O ângulo de bisel refere-se à inclinação usinada ou cortada na borda de apenas uma das chapas. O ângulo de chanfro representa a abertura angular total.",
    },
    {
        "eixo": "Geometria de Juntas",
        "contexto": "Relação de Ângulos",
        "comando": "Em uma junta com chanfro em V simétrico onde ambas as chapas foram preparadas, a relação entre o ângulo do bisel e o ângulo do chanfro é:",
        "options": [
            "O ângulo do chanfro é a metade do ângulo do bisel.",
            "O ângulo do chanfro é igual ao ângulo do bisel.",
            "O ângulo do chanfro é o dobro do ângulo do bisel.",
            "Não há relação direta entre eles.",
        ],
        "correct": 2,
        "just": "Como o chanfro é simétrico em V, ambas as peças receberam o mesmo ângulo de bisel. Portanto, o ângulo total do chanfro é o dobro do ângulo de bisel.",
    },
]

# Inicialização das Variáveis de Controle no Session State
if "etapa" not in st.session_state:
    st.session_state.etapa = "identificacao"  # Pode ser: identificacao, quiz, resultado
if "questao_atual" not in st.session_state:
    st.session_state.questao_atual = 0
if "respostas_usuario" not in st.session_state:
    st.session_state.respostas_usuario = [None] * len(quiz_data)
if "nome_aluno" not in st.session_state:
    st.session_state.nome_aluno = ""

# ==========================================
# TELA 1: Identificação do Aluno
# ==========================================
if st.session_state.etapa == "identificacao":
    st.subheader("Identificação do Aluno")
    nome_input = st.text_input(
        "Nome Completo:", placeholder="Digite seu nome completo aqui..."
    )

    if st.button("Iniciar Exercício", type="primary"):
        if nome_input.strip() == "":
            st.warning("Por favor, preencha o seu nome para continuar.")
        else:
            st.session_state.nome_aluno = nome_input
            st.session_state.etapa = "quiz"
            st.rerun()

# ==========================================
# TELA 2: Navegação das Questões (Paginação)
# ==========================================
elif st.session_state.etapa == "quiz":
    idx = st.session_state.questao_atual
    q = quiz_data[idx]

    # Cabeçalho da questão
    st.markdown(
        f"<span style='color:#005088;font-size:14px;font-weight:bold;'>[{q['eixo']}] Questão {idx + 1} de {len(quiz_data)}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(f"*{q['contexto']}*")
    st.markdown(f"**{q['comando']}**")

    # Exibição das alternativas
    resposta_selecionada = st.radio(
        "Selecione uma alternativa:",
        options=q["options"],
        index=None,
        label_visibility="collapsed",
    )

    st.divider()

    # Controle de botões (Avançar ou Finalizar)
    if st.button(
        "Confirmar e Avançar" if idx < len(quiz_data) - 1 else "Finalizar Exercício"
    ):
        if resposta_selecionada is None:
            st.warning("Selecione uma alternativa antes de avançar.")
        else:
            # Salva o índice da resposta escolhida
            indice_resposta = q["options"].index(resposta_selecionada)
            st.session_state.respostas_usuario[idx] = indice_resposta

            # Vai para a próxima ou encerra
            if idx < len(quiz_data) - 1:
                st.session_state.questao_atual += 1
            else:
                st.session_state.etapa = "resultado"

            st.rerun()

# ==========================================
# TELA 3: Resultados, Justificativas e Envio Nativo
# ==========================================
elif st.session_state.etapa == "resultado":
    st.header("Relatório do Exercício de Fixação")

    # Cálculo da Nota
    acertos = 0
    for i, q in enumerate(quiz_data):
        if st.session_state.respostas_usuario[i] == q["correct"]:
            acertos += 1

    total = len(quiz_data)
    pct = (acertos / total) * 100
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    st.success(f"**Aluno:** {st.session_state.nome_aluno} | **Data:** {data_atual}")
    st.markdown(f"### Acertos: {acertos} / {total} ({pct:.1f}%)")

    if pct >= 80:
        st.info("Excelente retenção de conhecimento!")
    elif pct >= 60:
        st.warning("Bom trabalho. Revise as justificativas das questões que errou.")
    else:
        st.error("Atenção: Revise os conceitos fundamentais de simbologia AWS.")

    st.divider()
    st.subheader("Revisão das Questões")

    # Exibe o feedback visual de cada questão para o aluno
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

    # Lógica de Envio Nativo via Python (smtplib)
    if st.button("Enviar Exercício ao Professor", type="primary"):
        with st.spinner("Conectando ao servidor de e-mail..."):
            try:
                # 1. Resgata as credenciais do gerenciador de segredos do Streamlit
                email_remetente = st.secrets["EMAIL_REMETENTE"]
                email_senha = st.secrets["EMAIL_SENHA"]
                email_destino = st.secrets["EMAIL_DESTINO"]

                # 2. Constrói o e-mail
                msg = EmailMessage()
                msg["Subject"] = f"Resultado Exercício - {st.session_state.nome_aluno}"
                msg["From"] = email_remetente
                msg["To"] = email_destino

                # Corpo do e-mail
                conteudo_email = f"""
Relatório de Exercício de Fixação

Aluno: {st.session_state.nome_aluno}
Disciplina: Preparação para Processos de Corte e Soldagem
Data: {data_atual}

Nota: {acertos} de {total} ({pct:.1f}%)
                """
                msg.set_content(conteudo_email)

                # 3. Conexão com o servidor SMTP (Configurado para Gmail)
                servidor_smtp = "smtp.gmail.com"
                porta = 587

                with smtplib.SMTP(servidor_smtp, porta) as server:
                    server.starttls()  # Inicia criptografia TLS
                    server.login(email_remetente, email_senha)
                    server.send_message(msg)

                st.success(
                    "✅ E-mail enviado com sucesso diretamente para sua caixa de entrada!"
                )

            except Exception as e:
                st.error(f"❌ Ocorreu um erro técnico ao tentar enviar o e-mail: {e}")
