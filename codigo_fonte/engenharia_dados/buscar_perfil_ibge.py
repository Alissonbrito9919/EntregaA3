import pandas as pd
import os
import requests

print("Iniciando Estratégia Avançada: Extração por Blocos Estaduais (SP/MG)...")

#Caminhos dos arquivos
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
pasta_dados = os.path.join(diretorio_atual, 'dados')
caminho_dataset = os.path.join(pasta_dados, 'dataset_ia_completo.csv')

if not os.path.exists(caminho_dataset):
    print(f"ERRO: Não encontrei o arquivo {caminho_dataset}.")
else:
    #Carrega o dataset unificado
    df_principal = pd.read_csv(caminho_dataset, sep=';', encoding='latin-1')
    
    #Códigos de abrangência estadual no IBGE (35 = São Paulo, 31 = Minas Gerais)
    estados_alvo = {"35": "SP", "31": "MG"}
    
    dict_renda = {}
    dict_idade = {}

    for cod_estado, sigla in estados_alvo.items():
        print(f"\n-> Puxando dados socioeconômicos direto do Censo para o estado: {sigla}")
        
        #URL de Renda para TODOS os municípios daquele estado específico (N6 de uma N3)
        url_renda = f"https://servicodados.ibge.gov.br/api/v3/agregados/9541/periodos/2022/variaveis/10614?localidades=N6[in%20N3[{cod_estado}]]"
        #URL de Idade para TODOS os municípios daquele estado específico
        url_idade = f"https://servicodados.ibge.gov.br/api/v3/agregados/9514/periodos/2022/variaveis/12803?localidades=N6[in%20N3[{cod_estado}]]"
        
        #Extraindo Renda do Estado
        try:
            res = requests.get(url_renda)
            if res.status_code == 200:
                resultados = res.json()[0]['resultados'][0]['series']
                for item in resultados:
                    dict_renda[str(item['localidade']['id'])] = item['serie']['2022']
                print(f"   [OK] Dados de Renda de {sigla} importados.")
            else:
                print(f"   [ERRO] API Renda {sigla} retornou status: {res.status_code}")
        except Exception as e:
            print(f"   [FALHA] Não foi possível ler Renda de {sigla}: {e}")

        #Extraindo Idade do Estado
        try:
            res = requests.get(url_idade)
            if res.status_code == 200:
                resultados = res.json()[0]['resultados'][0]['series']
                for item in resultados:
                    dict_idade[str(item['localidade']['id'])] = item['serie']['2022']
                print(f"   [OK] Dados de Idade de {sigla} importados.")
            else:
                print(f"   [ERRO] API Idade {sigla} retornou status: {res.status_code}")
        except Exception as e:
            print(f"   [FALHA] Não foi possível ler Idade de {sigla}: {e}")

    
    # MAPEANDO AS COLUNAS NO DATASET
    
    print("\nAlinhando dados do Censo com os municípios da tabela...")
    
    #Garante correspondência exata de tipo (texto puro)
    df_principal['CD_MUNICIPIO_IBGE'] = df_principal['CD_MUNICIPIO_IBGE'].astype(int).astype(str)
    
    df_principal['RENDA_PER_CAPITA'] = df_principal['CD_MUNICIPIO_IBGE'].map(dict_renda)
    df_principal['IDADE_MEDIANA'] = df_principal['CD_MUNICIPIO_IBGE'].map(dict_idade)
    
    #Conversão para numérico (limpando caracteres do IBGE como '...' se houver)
    df_principal['RENDA_PER_CAPITA'] = pd.to_numeric(df_principal['RENDA_PER_CAPITA'], errors='coerce')
    df_principal['IDADE_MEDIANA'] = pd.to_numeric(df_principal['IDADE_MEDIANA'], errors='coerce')
    
    #Preenchimento inteligente de segurança por média caso alguma cidade fique nula
    df_principal['RENDA_PER_CAPITA'] = df_principal.groupby('SG_UF')['RENDA_PER_CAPITA'].transform(lambda x: x.fillna(x.mean()))
    df_principal['IDADE_MEDIANA'] = df_principal.groupby('SG_UF')['IDADE_MEDIANA'].transform(lambda x: x.fillna(x.mean()))

    print("\n--- MATRIZ FINAL DE ATRIBUTOS PARA A INTELIGÊNCIA ARTIFICIAL ---")
    print(df_principal[['NM_MUNICIPIO', 'SG_UF', 'POPULACAO_2022', 'RENDA_PER_CAPITA', 'IDADE_MEDIANA', 'PERC_DESCONTENTES']].head())

    #Salva por cima com os dados reais e definitivos
    df_principal.to_csv(caminho_dataset, index=False, sep=';', encoding='latin-1')
    print(f"\n[SUCESSO] Arquivo 'dataset_ia_completo.csv' enriquecido com dados reais de SP e MG!")
    