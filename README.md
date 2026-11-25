#  Agrometeorologia de Londrina (PR)

Este repositório contém o projeto final da disciplina **Computação Aplicada às Ciências Atmosféricas II** (UEMA). O objetivo é analisar o clima de Londrina (PR) entre 1991 e 2020 e gerar um **dashboard interativo** de apoio à decisão agrícola.

## Sobre o Projeto

*   **Local de estudo:** Londrina (PR) - Estação INMET 83766.
*   **Período dos dados:** 01/01/1991 a 31/12/2020.
*   **Variáveis:** Precipitação, Temperatura (Máx, Média, Mín), Umidade e Vento.
*   **Fonte dos dados:** [INMET - BDMEP](https://bdmep.inmet.gov.br/)

## Acesso ao Dashboard

O produto final pode ser acessado online através do link abaixo:
**[Clique aqui para acessar o Dashboard](https://projeto-londrina-hqs9wd8btfiptenmleijsd.streamlit.app/)**

## Tecnologias Utilizadas

*   **Linguagem:** Python 
*   **Processamento de Dados:** Pandas, NumPy
*   **Visualização:** Matplotlib, Plotly
*   **Desenvolvimento Web:** Streamlit
*   **Ambiente:** Google Colab

##  Estrutura do Repositório

*   `app.py`: Código principal do dashboard (Streamlit).
*   `londrina_resumo_agricola.csv`: Dados mensais processados (médias e riscos).
*   `londrina_diario_tratado.csv`: Dados diários limpos e com falhas preenchidas.
*   `janelas_agricolas.png`: Gráfico de chuva mensal vs. janelas de plantio/colheita.
*   `requirements.txt`: Bibliotecas necessárias para rodar o app.

👩‍🔬 Autores
Stephany Albuquerque	
Yasmim Lorrane	
Ana Beatriz	
Pablo Ryan	
