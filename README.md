# Agente de IA para Classificação de Perfis Eleitorais

Este repositório contém o código-fonte de um agente preditivo desenvolvido em Python para inferir a propensão eleitoral de indivíduos com base em recortes sociodemográficos e regionais.O projeto mitiga o desequilíbrio de classes presente em dados públicos através do algoritmo CatBoost combinado a funções de custo balanceadas.

## Diferenciais Técnicos e Metodologia

**Cruzamento de Dados Públicos:** Integração e unificação de históricos de votação do TSE (Eleições 2022) com indicadores sociais e demográficos do Censo do IBGE[cite: 51].
**Engenharia de Recursos Granular:** Refinamento de variáveis como escolaridade e localização geográfica para aumentar o poder de discriminação do modelo.
**Validação por Prova Cega Geográfica:** O modelo foi treinado com dados de 25 estados e testado nos estados isolados de São Paulo e Minas Gerais, garantindo a capacidade de generalização com dados nunca antes vistos pela IA.
**Ajuste de Pesos Inversos:** Uso do hiperparâmetro `auto_class_weights='Balanced'` para neutralizar o viés da classe majoritária, permitindo mapear a minoria propensa à Terceira Via, Brancos e Nulos.

## Tecnologias Utilizadas

* [cite_start]Python 3 [cite: 72]
* [cite_start]CatBoost Classifier [cite: 50, 75]
* [cite_start]Pandas [cite: 75]
* Scikit-Learn
* Joblib

## Instruções de Instalação e Execução

### 1. Clonar o repositório
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
2. Instalar as dependências oficiais
Bash
pip install -r requirements.txt
3. Executar o Agente de IA no terminal
Bash
python codigo_fonte/app.py
