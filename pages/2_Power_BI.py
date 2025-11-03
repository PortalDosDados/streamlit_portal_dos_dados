import streamlit as st


# Configurações da página
st.set_page_config(
    page_title='Dione Nascimento - Power BI',       # Título da aba
    page_icon='assets/power_bi.png',   # Ícone da aba (pode ser .ico, .png ou emoji)
    layout='wide'                        # Layout da página (opcional)
)

st.image('assets/power_bi.png', width= 160)
st.header('Power BI')
st.markdown('''
O **Power BI** tem sido a minha principal escolha para visualziação de dados, 
é uma ferramenta simples de utilizar,além de ser a mais utilizado nesse seguimento.
Seguem alguns projetos que fiz e que posso compatilhar, a maior parte dos meus trabalhos foram realizados 
para a empresa que atuo hoje, não podendo compartilhar aqui.
''')

st.subheader('Dashboard Logístico Interativo')
st.markdown('''
Este dashboard foi desenvolvido para fornecer uma análise completa do desempenho logístico e 
financeiro de uma operação de transporte, com foco nos dados consolidados do ano de 2022.
O objetivo principal é centralizar indicadores-chave (KPIs) de forma visual e interativa, 
permitindo uma tomada de decisão rápida e baseada em dados para otimizar custos e melhorar 
a eficiência operacional.
''')

# Criando três colunas para as imagens
col1, col2, col3 = st.columns(3)

with col1:
    st.image('./assets/log_01.png', width=700)

with col2:
    st.image('./assets/log_02.png', width=700)

with col3:
    st.image('./assets/log_03.png', width=700)


st.subheader('Principais Análises e Recursos do Painel')

st.markdown('''

- **Visão Financeira Consolidada**:

    - Os cartões superiores destacam os três pilares financeiros da operação:

    - Lucro Total: R$ 4.406.005,52;

    - Custo Total: R$ 800.977,35;

    - Custo Fixo: R$ 174.061,94;

- **Desempenho Operacional Mensal (Quantidade de Viagens)**:

    - O gráfico de barras monitora o volume de viagens mês a mês, permitindo identificar sazonalidades. O pico operacional ocorreu em julho, com 2,9 mil viagens.

    - Ao interagir com o gráfico (como visto na imagem 3), é possível ver o detalhamento total de entregas (23.690), segmentadas entre Entregas no Prazo (17.086) e Entregas Atrasadas (6.604).

- **KPI de Eficiência (Entregas no Prazo)**:

    - Um medidor (gauge) dedicado monitora um dos KPIs mais críticos da logística.

    - O desempenho atual é de 72,12% de entregas no prazo, indicando um ponto de atenção, pois está abaixo da meta estabelecida de 85%.

- **Análise Detalhada de Custos de Manutenção**:

    Esta seção aprofunda a análise de uma das principais fontes de custo variável: a manutenção da frota, que totalizou R$ 194.960,07.

    O dashboard divide esse custo por Marca de Veículo, (sendo a Mercedes-Benz a de maior custo, com 59,1 mil Reais) e por Tipo de Veículo (liderado pelo TOCO, com 17,3 mil Reais).

    Os tooltips interativos (vistos na imagem 2) permitem detalhar ainda mais os custos operacionais, como Combustível e KMs Rodados, para análises mais granulares.
               
''')



st.subheader('Dashboard de Execução Financeira (Setor Público)')
st.markdown('''
Este dashboard oferece uma visão executiva e detalhada da execução financeira, projetado 
especificamente para o monitoramento de um grande orçamento (neste caso, público ou corporativo).

O painel centraliza os principais indicadores de compromisso orçamentário (empenho) e pagamento, 
permitindo que os gestores analisem a performance financeira, 
identifiquem gargalos e entendam a distribuição dos gastos.
''')

# Criando duas colunas para as imagens
col1, col2, = st.columns(2)

with col1:
    st.image('./assets/fin_01.png', width=700)

with col2:
    st.image('./assets/fin_02.png', width=700)

st.subheader('Principais Análises e Recursos do Painel')


st.markdown('''
            
- **KPIs Financeiros Globais (Visão Macro)**:

    - Os cartões principais fornecem a situação imediata da execução:

    - Total Empenho: R$ 118,86 Bilhões (orçamento total comprometido).

    - Total A Pagar: R$ 4,00 Bilhões (valor empenhado, mas pendente de pagamento).

    - Total Pago: R$ 105,00 Bilhões (valor efetivamente desembolsado).

- **Indicador-Chave de Eficiência (KPI - % Empenho Pago)**:

    - Um medidor (gauge) destaca a principal métrica de eficiência da gestão.

    - O indicador mostra que 88,34% do valor empenhado foi pago, sinalizando um ponto de atenção por estar abaixo da meta de 95,00%.

- **Análise Histórica (Empenho vs. Pagamento)**:

    - O gráfico "Total Pago/Empenho - Ano/Mês" (exibindo anos) permite uma análise da evolução histórica.

    - Ele compara o volume total empenhado (azul) contra o total pago (laranja) ano a ano, facilitando a identificação de tendências e do gap financeiro (diferença entre o comprometido e o pago) ao longo do tempo.

''')


