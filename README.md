# 📊 Portal dos Dados - Portfólio Dione Nascimento

> "Quando não se agrega valor, se agrega custo."

Este repositório hospeda a aplicação web oficial do **Portal dos Dados**, desenvolvida em **Python** com **Streamlit**. 

O projeto serve como um hub central que conecta minha trajetória de 15 anos em Manutenção Industrial com soluções modernas de Ciência de Dados, além de direcionar para conteúdos educativos sobre Python, SQL, Power BI e Power Apps.

---

## 🎯 Objetivo do Projeto

Demonstrar na prática como ferramentas de *Data Science* podem ser aplicadas para criar interfaces profissionais e interativas, servindo como:
1.  **Portfólio Profissional:** Apresentação de trajetória e especialidades (Confiabilidade, Siderurgia, BI).
2.  **Hub de Conteúdo:** Centralização de links e recursos do canal "Portal dos Dados".
3.  **Demonstração Técnica:** Exemplo de uso de CSS customizado e injeção de HTML dentro do framework Streamlit.

## 🛠️ Tecnologias Utilizadas

* **Python 3.12+**: Linguagem base.
* **Streamlit**: Framework para construção da interface web.
* **CSS3 & HTML5**: Customização avançada de estilo (arquivo `style.css` injetado) para botões, cards e tipografia.
* **Pandas**: (Para manipulação de dados nas páginas internas).

## 📂 Estrutura do Projeto

A organização segue as melhores práticas para aplicações *Streamlit Multipage*:

```text
/
├── .venv/                  # Ambiente Virtual (Ignorado pelo Git)
├── assets/                 # Imagens estáticas (logos, fotos, banners)
├── data/                   # Arquivos de dados (CSV, Excel) para dashboards
├── pages/                  # Sub-páginas da aplicação (Dashboards, Ferramentas)
├── .gitignore              # Arquivo de segurança e exclusão
├── Dione_Nascimento.py     # 🏠 PÁGINA INICIAL (Main Script)
├── requirements.txt        # Lista de dependências
├── style.css               # Folha de estilos personalizada
└── README.md               # Documentação