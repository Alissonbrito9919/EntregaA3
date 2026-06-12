import pandas as pd
import glob
import os

print("Iniciando o Pipeline TSE (Foco: Brancos e Nulos para Governador em SP/MG)...")

# 1. Definição do caminho exato da sua estrutura
pasta_apuracao = os.path.join('código_fonte', 'dados', 'detalhe_votacao_munzona_2022')
arquivos = glob.glob(os.path.join(pasta_apuracao, '*.csv'))
lista_dfs = []

if not arquivos:
    print(f"ERRO: Nenhum arquivo .csv encontrado em: {pasta_apuracao}")
else:
    for arquivo in arquivos:
        print(f"Processando: {os.path.basename(arquivo)}...")
        
        try:
            df = pd.read_csv(
                arquivo, 
                sep=None, 
                engine='python', 
                encoding='latin-1', 
                on_bad_lines='skip',
                memory_map=True 
            )
            
            # Garantindo o tratamento do texto da coluna
            if 'DS_CARGO' in df.columns:
                df['DS_CARGO'] = df['DS_CARGO'].astype(str).str.upper().str.strip()
                
                # MUDANÇA CRUCIAL: Filtrando por GOVERNADOR, que está presente no seu arquivo!
                df = df[df['DS_CARGO'] == 'GOVERNADOR']
            
            lista_dfs.append(df)
            
        except Exception as e:
            print(f"--- ERRO AO LER {os.path.basename(arquivo)}: {e}")
            continue

    # 3. Consolidação dos dados
    if lista_dfs:
        print("\nAgrupando e somando os dados por município...")
        df_consolidado = pd.concat(lista_dfs, ignore_index=True)
        
        # Conversão segura para numérico
        cols_to_numeric = ['CD_MUNICIPIO', 'QT_APTOS', 'QT_VOTOS_BRANCOS', 'QT_VOTOS_NULOS']
        for col in cols_to_numeric:
            if col in df_consolidado.columns:
                df_consolidado[col] = pd.to_numeric(df_consolidado[col], errors='coerce')
        
        # 4. Agrupamento por Município (Soma as zonas eleitorais da mesma cidade)
        df_municipios = df_consolidado.groupby(['SG_UF', 'CD_MUNICIPIO', 'NM_MUNICIPIO']).agg({
            'QT_APTOS': 'sum',
            'QT_VOTOS_BRANCOS': 'sum',
            'QT_VOTOS_NULOS': 'sum'
        }).reset_index()
        
        # 5. Criação da Métrica de Descontentamento
        df_municipios['TOTAL_BRANCO_NULO'] = df_municipios['QT_VOTOS_BRANCOS'] + df_municipios['QT_VOTOS_NULOS']
        df_municipios['PERC_DESCONTENTES'] = (df_municipios['TOTAL_BRANCO_NULO'] / df_municipios['QT_APTOS']) * 100
        
        print("\n--- AMOSTRA DA BASE CONSOLIDADA (SP + MG) ---")
        print(df_municipios[['NM_MUNICIPIO', 'SG_UF', 'QT_APTOS', 'PERC_DESCONTENTES']].head())
        
        # Salvando o seu arquivo de teste cego
        df_municipios.to_csv('tse_teste_sp_mg.csv', index=False, sep=';', encoding='latin-1')
        print(f"\nSucesso! Arquivo 'tse_teste_sp_mg.csv' gerado com {df_municipios.shape[0]} cidades.")
    else:
        print("Erro: Nenhuma linha de Governador foi processada.")