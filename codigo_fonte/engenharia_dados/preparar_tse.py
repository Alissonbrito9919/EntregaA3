import pandas as pd

print("Iniciando a extração da base do TSE...")

caminho_1t = 'código_fonte/dados/Historico_Totalizacao_Presidente_BR_1T_2022.csv' 
caminho_2t = 'código_fonte/dados/Historico_Totalizacao_Presidente_BR_2T_2022.csv'

try:
    #Lendo o 1º Turno (Aplicando as regras do LEIA-ME do TSE: separador ';' e encoding 'latin1')
    print("Lendo estrutura do 1º Turno...")
    df_1t = pd.read_csv(caminho_1t, sep=';', encoding='latin1', nrows=1000)
    
    #Lendo o 2º Turno
    print("Lendo estrutura do 2º Turno...")
    df_2t = pd.read_csv(caminho_2t, sep=';', encoding='latin1', nrows=1000)

    print("\nSUCESSO! Os arquivos foram abertos no Pandas.")
    print("Aqui estão as colunas que o TSE nos forneceu no 1º turno:")
    print(df_1t.columns.tolist())
    
except FileNotFoundError:
    print("Erro: O Python não encontrou o arquivo. Verifique se o nome e o caminho da pasta estão idênticos ao arquivo que você extraiu.")