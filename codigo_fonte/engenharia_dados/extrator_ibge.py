import requests
import pandas as pd
import os

print("Conectando à API do Censo 2022 do IBGE (Pesquisa 10101)...")

#ID 4714 é a tabela de População Residente do Censo 2022
#Variável 93 é a População. N6[all] significa: trazer de TODOS os municípios do Brasil.
id_tabela = "4714"
url_ibge = f"https://servicodados.ibge.gov.br/api/v3/agregados/{id_tabela}/periodos/2022/variaveis/93?localidades=N6[all]"

try:
    #Faz a chamada HTTP direto para os servidores do IBGE
    resposta = requests.get(url_ibge)
    
    if resposta.status_code == 200:
        print("Conexão bem-sucedida! Extraindo e tratando o JSON...")
        dados_json = resposta.json()
        
        #O JSON do IBGE vem em camadas (aninhado). Vamos varrer a estrutura para criar nossa lista:
        resultados = dados_json[0]['resultados'][0]['series']
        
        linhas = []
        for item in resultados:
            codigo_municipio = item['localidade']['id']
            nome_municipio = item['localidade']['nome']
            populacao = item['serie']['2022']
            linhas.append([codigo_municipio, nome_municipio, populacao])
            
        #Montando o DataFrame do Pandas
        df_ibge = pd.DataFrame(linhas, columns=['CD_MUNICIPIO_IBGE', 'NM_MUNICIPIO_IBGE', 'POPULACAO_2022'])
        
        print("\n--- AMOSTRA DOS DADOS EXTRAÍDOS DO CENS0 ---")
        print(df_ibge.head())
        
        #Salvando o arquivo CSV na raiz do projeto
        df_ibge.to_csv('ibge_populacao_municipios.csv', index=False)
        print("\nArquivo 'ibge_populacao_municipios.csv' gerado com sucesso!")
        
    else:
        print(f"A API do IBGE retornou um erro. Status Code: {resposta.status_code}")

except Exception as e:
    print(f"Ocorreu um erro ao conectar com o IBGE: {e}")