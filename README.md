# 📊 Portal dos Dados - Portfólio Profissional

> **"Quando não se agrega valor, se agrega custo."**

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Online-brightgreen?style=for-the-badge)

## 📖 Sobre o Projeto

Este repositório hospeda a aplicação web oficial do **Portal dos Dados**, desenvolvida inteiramente em **Python** utilizando o framework **Streamlit**.

O projeto atua como um hub central que materializa minha trajetória de **15 anos em Manutenção Industrial** (Siderurgia e Confiabilidade) integrada com soluções modernas de **Ciência de Dados**. Aqui, convergem a técnica da engenharia e a inteligência dos dados.

---

## 🎯 Objetivos da Aplicação

Esta aplicação não é apenas um currículo, é uma demonstração técnica de capacidade:

* ✅ **Portfólio Vivo:** Apresentação interativa de especialidades, certificações e cases de sucesso.
* ✅ **Hub de Conteúdo:** Centralização de recursos educativos sobre Python, SQL, Power BI e Power Apps do canal.
* ✅ **Showcase de Frontend:** Demonstração avançada de como injetar **CSS3 e HTML5** no Streamlit para fugir do padrão e criar interfaces únicas.

---

## 🛠️ Tech Stack

* **Linguagem:** `Python 3.12+`
* **Framework Web:** `Streamlit`
* **Estilização:** `CSS3` (Injeção customizada via `style.css`) & `HTML5`
* **Manipulação de Dados:** `Pandas`
* **Visualização:** `Plotly` / `Streamlit Charts`

---

## 📂 Estrutura do Repositório

A organização dos arquivos reflete o ambiente de desenvolvimento atual:

```text
STREAMLIT_PORTAL_DOS_DADOS/
├── .venv/                  # Ambiente Virtual (Ignorado no Git)
├── assets/                 # Recursos estáticos (Imagens, Logos, Banners)
├── data/                   # Bases de dados para os dashboards
├── pages/                  # Páginas da aplicação (Multipage)
│   ├── 2_Power_BI.py       # Dashboard de Power BI
│   ├── 3_Power_App.py      # Integração com Power Apps
│   └── 4_Python.py         # Scripts e Ferramentas Python
├── .gitattributes          # Configurações de atributos do Git
├── .gitignore              # Arquivo de exclusão do Git
├── Dione_Nascimento.py     # 🏠 SCRIPT PRINCIPAL (Home Page)
├── README.md               # Documentação do projeto
├── requirements.txt        # Lista de dependências
└── style.css               # Customização visual (CSS)

---

## 📝 Corretor Automático de Gabaritos (Nova funcionalidade)

Esta aplicação inclui um módulo de correção automática de gabaritos OMR (optical
mark recognition) projetado para funcionar inteiramente em uma única página A4.

- Layout: o gerador de gabarito monta as questões em colunas, com no máximo
	25 linhas por coluna (variável `max_linhas_coluna = 25`). O PDF é gerado via
	`ReportLab` como uma única página A4 contendo 4 marcadores fiduciários nos
	cantos para garantir o alinhamento por `OpenCV`.
- Processamento: a função `processar_imagem_opencv` detecta os marcadores,
	aplica correção de perspectiva, binariza a região de leitura e divide a
	grade em colunas/linhas para extrair as 5 alternativas por questão.
- Auditoria Visual: o front-end em Streamlit agora exibe duas imagens de
	depuração após a correção: a imagem alinhada (RGB) e a grade binarizada
	(preto e branco) para facilitar verificação manual.

### Como usar (resumo rápido)

1. Em *Configuração* defina a `Quantidade de Questões` e salve o `Gabarito Oficial`.
2. Clique em *Gerar Folha Padrão* para baixar o PDF A4 (imprima em página única).
3. Preencha a prova impressa, fotografe alinhando os 4 cantos marcados ou envie o arquivo.
4. Clique em *Executar Correção da Prova* — o sistema retornará a nota, o log
	 de correção e as imagens de auditoria para inspeção.

### Dependências relevantes

As dependências principais para este módulo são:

```
reportlab
opencv-python
Pillow
numpy
streamlit
```

Adicione ao `requirements.txt` se necessário e instale com:

```bash
pip install -r requirements.txt
```
