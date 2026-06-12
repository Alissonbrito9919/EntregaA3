# Agente de IA para Classificação de Perfis Eleitorais

[cite_start]Este repositório contém o código-fonte de um agente preditivo desenvolvido em Python para inferir a propensão eleitoral de indivíduos com base em recortes sociodemográficos e regionais[cite: 45, 48, 59]. [cite_start]O projeto mitiga o desequilíbrio de classes presente em dados públicos através do algoritmo CatBoost combinado a funções de custo balanceadas[cite: 50].

## Diferenciais Técnicos e Metodologia

* [cite_start]**Cruzamento de Dados Públicos:** Integração e unificação de históricos de votação do TSE (Eleições 2022) com indicadores sociais e demográficos do Censo do IBGE[cite: 51].
* [cite_start]**Engenharia de Recursos Granular:** Refinamento de variáveis como escolaridade e localização geográfica para aumentar o poder de discriminação do modelo[cite: 51, 63].
* [cite_start]**Validação por Prova Cega Geográfica:** O modelo foi treinado com dados de 25 estados e testado nos estados isolados de São Paulo e Minas Gerais, garantindo a capacidade de generalização com dados nunca antes vistos pela IA[cite: 52, 73].
* [cite_start]**Ajuste de Pesos Inversos:** Uso do hiperparâmetro `auto_class_weights='Balanced'` para neutralizar o viés da classe majoritária, permitindo mapear a minoria propensa à Terceira Via, Brancos e Nulos[cite: 50, 76].

## Desempenho e Resultados do Modelo

[cite_start]Na Prova Cega Geográfica, o agente alcançou uma Acurácia Geral de 75,58% e um F1-Score médio de 0,60 (Macro Avg), avaliado em uma base com 10.000 amostras reais de teste[cite: 52, 55, 66].

### Relatório Detalhado de Classificação

| Classe Alvo | Precisão (Precision) | Sensibilidade (Recall) | F1-Score | Amostras (Support) |
| :--- | :---: | :---: | :---: | :---: |
| Voto em Polos | [cite_start]0,84 [cite: 58] | [cite_start]0,86 [cite: 58] | 0,85 | 8.049 |
| Terceira Via / Branco / Nulo | [cite_start]0,37 [cite: 65] | [cite_start]0,34 [cite: 65] | 0,35 | 1.951 |
| **Acurácia Geral do Agente** | — | — | [cite_start]**0,76** [cite: 52] | [cite_start]**10.000** [cite: 55] |
| **Média Geral (Macro Avg)** | **0,60** | **0,60** | [cite_start]**0,60** [cite: 66] | [cite_start]**10.000** [cite: 55] |

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
