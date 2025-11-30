import streamlit as st

# Configurações da página
st.set_page_config(
    page_title='Portal dos Dados - Power Apps',
    page_icon='assets/power_apps.png',
    layout='wide'     # Layout da página
)

#CSS
with open('style.css', 'r', encoding='utf-8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- Seção do Header ---
st.image('assets/power_apps.png', width=160)
st.header('Power Apps')
st.markdown('''
<div class='justificado'>
    O Power Apps é o meu 'canivete suíço' para digitalização de processos. Quando
    vejo uma rotina que pode ser otimizada, como um formulário de papel ou uma planilha
    confusa, vejo uma oportunidade para um app.
    <br><br>
    Gosto da plataforma pela sua rapidez em criar soluções robustas que se integram perfeitamente
    ao ecossistema Microsoft. O objetivo é sempre o mesmo:
    <br><br>
    <div style='text-align: center; font-style: italic; color: #185'>
        'Facilitar a vida do usuário na ponta e gerar dados mais limpos para a gestão.'
    </div>
    <br>
    Abaixo estão alguns projetos que construí.
</div>
''', unsafe_allow_html=True)

st.divider()

st.subheader('Aplicativo de Catálogo para Lubrificantes')
st.video('https://www.youtube.com/watch?v=MNXcNj8PiOU')




st.divider()

st.subheader('Aplicativo de Inspeção em Equipamentos')
st.video('https://www.youtube.com/watch?v=ZH-m1hMfzvM&t=23s')


st.subheader('Controle de Ferramentaria')
st.markdown('''
<div class='justificado'>
O objetivo principal do aplicativo é rastrear o inventário de ferramentas,
gerenciar quem as utiliza e saber seu status atual.
</div>
''', unsafe_allow_html=True)

# --- Galeria de Imagens ---
st.subheader('Visão Geral do Aplicativo')

# Criando quatro colunas para as imagens
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image(
        './assets/app_ferr_01.jpeg',
        caption='1. Tela Inicial (Boas-vindas)',

    )

with col2:
    st.image(
        './assets/app_ferr_02.jpeg',
        caption='2. Tela de Lista (Inventário)',

    )

with col3:
    st.image(
        './assets/app_ferr_03.jpeg',
        caption='3. Tela de Detalhes (Visualização)',

    )

with col4:
    st.image(
        './assets/app_ferr_04.jpeg',
        caption='4. Tela de Edição (Empréstimo)',

    )


# --- Descrição Detalhada ---
st.subheader('Funcionalidades de Cada Tela')

# AJUSTE: Usar 'expanders' para organizar o texto
with st.expander('**1. Tela Inicial (Boas-vindas)**'):
    st.markdown('''
    * **Propósito:** É a tela de entrada do aplicativo.
    * **Recursos:**
        * Mostra uma saudação personalizada ao usuário logado ('Olá + nome do usuário').
        * Possui um botão claro ('Toque para Começar') para navegar para a próxima tela.
        * Identifica o desenvolvedor ('Desenvolvido por: Dione Nascimento (esse aqui escrevendo)').
    ''')

with st.expander('**2. Tela de Lista (Inventário)**'):
    st.markdown('''
    * **Propósito:** Apresentar um inventário de todas as ferramentas cadastradas.
    * **Recursos:**
        * **Barra de Busca:** Permite ao usuário encontrar uma ferramenta específica rapidamente.
        * **Galeria de Ferramentas:** É a lista principal. Cada item mostra:
            * Uma imagem da ferramenta.
            * O nome da ferramenta (ex: 'Chave de boca', 'Marreta', 'Máquina de solda').
            * O **Status** atual (ex: 'Disponível', 'Em conserto', 'Queimado').
        * **Botão de Adicionar ('+'):** Usado para cadastrar novas ferramentas no inventário.
    ''')

with st.expander('**3. Tela de Detalhes (Modo de Visualização)**'):
    st.markdown('''
    * **Propósito:** Mostrar todas as informações de uma ferramenta específica que foi selecionada na tela anterior.
    * **Recursos:**
        * Exibe a foto da ferramenta em destaque.
        * Mostra todos os campos de informação em modo 'somente leitura':
            * Status: Disponível
            * Modelo: 5Kgs
            * Data de empréstimo: 25/11/2024
            * Nome do solicitante: Ferramentaria (indicando que esta no estoque).
            * Observações da condição: (vazio)
    ''')

with st.expander('**4. Tela de Edição (Modo de Empréstimo/Devolução)**'):
    st.markdown('''
    * **Propósito:** Esta é a tela de ação, usada para editar os detalhes de uma ferramenta, e o mais importante: registrar um empréstimo (check-out) ou devolução (check-in).
    * **Recursos:**
        * Os campos agora são editáveis (caixas de texto, listas suspensas, seletores de data/hora).
        * **Controle de Empréstimo:** O usuário pode:
            * Mudar o Status ('Disponível' para 'Emprestado').
            * Digitar o Nome do solicitante.
            * Registrar a Data de empréstimo e a Data de devolução prevista.
            * Adicionar Observações (ex: 'ferramenta com pequena avaria').
        * **Ícones de Ação:**
            * 'X' (Cancelar): Descarta as alterações.
            * '✓' (Salvar): Confirma as alterações e atualiza o status da ferramenta no sistema.
    ''')


# --- DIVISOR ENTRE OS PROJETOS ---
st.divider()

# --- PROJETO 2: GERENCIAMENTO DE PENDÊNCIAS ---

st.header('Aplicativo de Gerenciamento de Pendências')
st.markdown('''
Este aplicativo funciona como um sistema de rastreamento de tarefas ou problemas
(como ordens de serviço) para equipes operacionais ou de manutenção.
''')

# --- Galeria de Imagens App 2 ---
st.subheader('Visão Geral do Aplicativo')

# Criando quatro colunas para as imagens
col1, col2, col3 = st.columns(3)

with col1:
    st.image(
        './assets/app_pend_01.jpeg',
        caption='1. Tela Inicial (Boas-vindas)',

    )

with col2:
    st.image(
        './assets/app_pend_02.jpeg',
        caption='2. Tela de Lista (Pendências)',

    )

with col3:
    st.image(
        './assets/app_pend_03.jpeg',
        caption='3. Tela de Formulário (Criar/Editar)',

    )



# --- Descrição Detalhada App 2 ---
st.subheader('Funcionalidades de Cada Tela')

with st.expander('**1. Tela Inicial (Boas-vindas)**'):
    st.markdown('''
    * **Propósito:** Tela de entrada padrão do aplicativo.
    * **Recursos:**
        * Saúda o usuário logado ('Olá + Nome do usuário').
        * Título claro: 'Gerenciamento de Pendências'.
        * Botão 'Toque para começar' para navegar à tela principal.
    ''')

with st.expander('**2. Tela de Lista (Lista de Solicitações)**'):
    st.markdown('''
    * **Propósito:** Apresentar um painel (dashboard) com todas as pendências registradas.
    * **Recursos:**
        * **Barra de Busca:** Permite ao usuário filtrar por uma pendência específica.
        * **Galeria de Pendências:** Lista os itens, mostrando:
            * O problema (ex: 'Motor queimado').
            * O responsável (ex: 'Miguel Filho').
            * A data de registro ou prazo.
            * Um status visual (ex: 'ATRASADO').
        * **Botões de Ação:**
            * **'+' (Adicionar):** Leva à tela de formulário para criar uma nova pendência.
            * **Atualizar/Ordenar:** Para recarregar e organizar a lista.
    ''')

with st.expander('**3. Tela de Formulário (Solicitações Operacionais)**'):
    st.markdown('''
    * **Propósito:** Tela para criar ou editar uma solicitação/pendência.
    * **Recursos:**
        * **Campos Detalhados:** O usuário preenche todos os dados necessários para abrir um chamado:
            * `Área` (ex: Mistura)
            * `Tipo de solicitação` (ex: Falha)
            * `TAG do equipamento` (identificador único da máquina)
            * `Pendência` (descrição do problema)
            * `Responsável` (quem deve executar)
            * `Data de registro` e `Prazo`.
        * **Ícones de Ação:** 'X' (Cancelar) e '✓' (Salvar) para confirmar o registro no banco de dados.
    ''')
