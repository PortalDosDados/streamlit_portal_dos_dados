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

st.subheader('Dashboard Eleições Presidenciais')

st.markdown('''
Este projeto apresenta uma análise completa das eleições presidenciais no Brasil.
A ideia é transformar dados dispersos em uma visualização clara, organizada e útil para entender o comportamento do eleitorado em cada estado.

O painel mostra como os votos se distribuem pelo país, compara candidatos, destaca quem lidera em cada região e oferece uma visão geral dos números que realmente importam.
''')

st.subheader('Visualização do Dashboard')
st.markdown('''
Abaixo está o relatório interativo publicado no Power BI.
Ele permite explorar filtros de ano, turno e estado, além de analisar o desempenho de cada candidato ao longo do país.
''')

powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=d472eaa0-bed3-49e5-80ab-c6778977d0c6&autoAuth=true&ctid=da49a844-e2e3-40af-86a6-c3819d704f49"
st.components.v1.iframe(powerbi_url, height=900, scrolling=True)

st.subheader('Principais recursos e análises do painel')

st.markdown('''
- **Visão nacional de votos**  
  A distribuição dos votos por estado é apresentada em um mapa interativo.
  Facilita entender onde cada candidato performou melhor e como o voto se espalhou pelo país.

- **Comparação entre candidatos**  
  Um gráfico de barras mostra rapidamente quem lidera a disputa e com qual porcentagem.
  Ideal para comparar desempenho lado a lado.

- **Candidato mais votado**  
  O painel destaca automaticamente o mais votado com sua foto, partido e percentual de votos.

- **Ranking detalhado**  
  Uma tabela lista todos os candidatos, com número, partido e ano da eleição.
  Transparência total sobre quem concorreu e como ficou posicionado.

- **Treemap por estado**  
  Exibe o peso relativo de cada estado no total de votos.
  Mostra quem realmente puxa a eleição e onde estão os maiores colégios eleitorais.

- **Filtros interativos**  
  Permitem navegar por:
  - Ano  
  - Turno  
  - Estado  
  Tornando a análise dinâmica e ajustável ao cenário desejado.

Este painel transforma dados brutos das eleições em visualizações simples, rápidas e úteis, dando clareza ao processo eleitoral e permitindo explorar o comportamento do eleitor em cada canto do país.
''')



st.subheader('Dashboard Logístico Interativo')
st.markdown('''
Este dashboard foi desenvolvido para fornecer uma análise completa do desempenho logístico e 
financeiro de uma operação de transporte, com foco nos dados consolidados do ano de 2022.
O objetivo principal é centralizar indicadores-chave (KPIs) de forma visual e interativa, 
permitindo uma tomada de decisão rápida e baseada em dados para otimizar custos e melhorar 
a eficiência operacional.
''')

powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=b40c8b5e-e562-4591-b920-61884a06ae3e&autoAuth=true&ctid=da49a844-e2e3-40af-86a6-c3819d704f49"
st.components.v1.iframe(powerbi_url, height=900, scrolling=True)

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

powerbi_url = "https://www.youtube.com/watch?v=hQVrG6j-OMs"
st.components.v1.iframe(powerbi_url, height=900, scrolling=True)


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


st.subheader('Dashboard Análise da Folha de Pagamento')
st.markdown('''
Este projeto demonstra a construção de uma solução completa de Business Intelligence, 
cobrindo todo o pipeline de dados, desde a extração e transformação (ETL) até a 
modelagem de dados e a visualização final em um dashboard interativo.

O objetivo é analisar a folha de pagamento dos Funcionários Municipais de Fortaleza "PMF", 
fornecendo transparência e insights acionáveis sobre os custos com pessoal, 
distribuição salarial e estrutura organizacional.
''')

# Criando três colunas para as imagens
col1, col2, col3 = st.columns(3)

with col1:
    st.image('./assets/pmf_01.png', width=700)

with col2:
    st.image('./assets/pmf_02.jpg', width=700)

with col3:
    st.image('./assets/pmf_03.jpg', width=700)
    

st.subheader('Principais Análises e Recursos do Painel')

st.markdown('''
            
- **ETL (Extract, Transform, Load) com Pentaho**:
    - A base do projeto começa com a engenharia de dados, utilizando o Pentaho Data Integration (Spoon),
    foi construído um processo de ETL robusto;

    - Extração: Os dados brutos são lidos de uma fonte primária (Table input);

    - Transformação e Enriquecimento: O fluxo realiza várias operações de Database lookup para buscar 
    chaves e informações em tabelas auxiliares (como dimensão de cargo, pessoa, órgão, etc.);

    - Carga: Os dados limpos e estruturados são carregados em um Data Warehouse, preenchendo a tabela 
    fato_pagamento (Tabela Fato) e as tabelas de dimensão que a cercam;     
       
- **Modelagem de Dados (Data Warehouse)**:     
            
    - Após o ETL, os dados são armazenados de forma otimizada para análise, seguindo as melhores 
    práticas de modelagem;

    - Banco de Dados: Um banco de dados (PostgreSQL, visível na Imagem 2) armazena 
    as tabelas limpas. A Imagem 2 mostra a tabela fato_pagamento finalizada, já contendo as chaves 
    estrangeiras (id_pessoa, id_cargo, id_orgao) e as métricas (proventos, descontos, liquido);

    - Modelo Estrela (Star Schema): Dentro do Power BI (Imagem 3), os dados são organizados em um Modelo 
    Estrela perfeito;

    - Tabela Fato: A public.fato_pagamento fica no centro, contendo todas as métricas financeiras;

    - Tabelas Dimensão: Ela é cercada por dimensões que dão contexto aos dados (dim_orgao, dim_cargo, 
    dim_pessoa, dim_grau_de_instrucao, dim_tempo);

    - Este modelo é a fundação que garante a alta performance e a facilidade para criar as análises no dashboard;
                
- **Modelagem de Dados (Data Warehouse)**:  
    
    - A etapa final é a visualização (Imagem 1), onde os dados modelados são apresentados aos gestores para a 
    tomada de decisão:

    - KPIs Principais: O dashboard exibe uma visão macro imediata:

    - Total de Órgãos: 81

    - Total de Servidores: 66.310

    - Total de Proventos: R$ 451.963.336

- **Filtros Interativos: O usuário pode segmentar a análise por Ano, Mês, Órgão e Matrícula**.

    - Análises de Média Salarial;

    - Por Grau de Instrução (Treemap): Mostra visualmente a distribuição e a média salarial por 
    nível de formação, desde "Residência Médica" e "Doutorado" até "Ensino Primário";

    - Por Cargo (Gráfico de Barras): Ranqueia a média salarial por cargo, destacando os maiores valores,
    como "Consultor Tec Adm" (R\$ 68 mil) e "Procurador Geral" (R\$ 43 mil);

    - Tabela de Detalhes: Fornece uma visão granular em nível de servidor, permitindo a consulta de valores
    individuais de proventos, descontos e valor líquido, com a data de pagamento;
            
            
            
            
''')


