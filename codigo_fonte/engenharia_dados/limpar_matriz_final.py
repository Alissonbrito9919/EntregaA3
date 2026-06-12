import pandas as pd
import os

print("Blindando a Matriz de Dados Local para o Treinamento...")

#Caminhos dos arquivos
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
pasta_dados = os.path.join(diretorio_atual, 'dados')
caminho_dataset = os.path.join(pasta_dados, 'dataset_ia_completo.csv')

if not os.path.exists(caminho_dataset):
    print(f"ERRO: Não encontrei o arquivo {caminho_dataset}")
else:
    #Carrega a base atual
    df = pd.read_csv(caminho_dataset, sep=';', encoding='latin-1')
    
    #Como a API do IBGE caiu (Erro 500), removemos as colunas de Renda e Idade que ficaram com NaN
    #para não confundir o modelo matemático da IA
    df = df.drop(columns=['RENDA_PER_CAPITA', 'IDADE_MEDIANA'], errors='ignore')
    
    #Criamos uma nova variável preditiva (Feature Engineering) muito inteligente:
    #A proporção de eleitores em relação à população total da cidade
    df['PROP_ELEITORADO'] = (df['QT_APTOS'] / df['POPULACAO_2022']) * 100
    
    print("\n--- MATRIZ REAL E BLINDADA PARA O MODELO DE IA ---")
    print(df[['NM_MUNICIPIO', 'SG_UF', 'POPULACAO_2022', 'QT_APTOS', 'PROP_ELEITORADO', 'PERC_DESCONTENTES']].head())
    
    #Salva a base final limpa e sem erros
    df.to_csv(caminho_dataset, index=False, sep=';', encoding='latin-1')
    
    print(f"\n[PRONTO para o catboost] Arquivo limpo com sucesso!")
    print(f"Total de cidades prontas para a IA: {df.shape[0]}")