import pandas as pd
import os

print("Iniciando o Cruzamento Estratégico de Dados Inteligente (Treino vs Teste)...")

#Caminhos das pastas
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
pasta_dados = os.path.join(diretorio_atual, 'dados')

caminho_treino_tse = os.path.join(pasta_dados, 'tse_treino_25_estados.csv')
caminho_teste_tse = os.path.join(pasta_dados, 'tse_teste_sp_mg.csv')
caminho_ibge = os.path.join(pasta_dados, 'ibge_populacao_municipios.csv')

def cruzar_com_ibge(df_tse, df_ibge):
    df_ibge_copy = df_ibge.copy()
    df_tse_copy = df_tse.copy()
    
    #Padronizar
    df_tse_copy.columns = df_tse_copy.columns.str.upper().str.strip()
    
    #Mapeia dinamicamente onde estão os nomes e UFs
    col_municipio = 'NM_MUNICIPIO' if 'NM_MUNICIPIO' in df_tse_copy.columns else ('NM_MUNICIPIO_TSE' if 'NM_MUNICIPIO_TSE' in df_tse_copy.columns else None)
    col_uf = 'SG_UF' if 'SG_UF' in df_tse_copy.columns else ('UF' if 'UF' in df_tse_copy.columns else None)
    col_aptos = 'QT_APTOS' if 'QT_APTOS' in df_tse_copy.columns else ('QT_ELEITORES' if 'QT_ELEITORES' in df_tse_copy.columns else None)
    
    #Se não achou por nome padrão, pega as colunas textuais por eliminação
    if not col_municipio or not col_uf:
        print("Aviso: Mapeando colunas textuais por estrutura...")
        cols_str = df_tse_copy.select_dtypes(include=['object']).columns
        if len(cols_str) >= 2:
            col_uf = col_uf or cols_str[1]
            col_municipio = col_municipio or cols_str[0]

    #Prepara a CHAVE_JOIN no IBGE
    df_ibge_copy['NM_LIMPO'] = df_ibge_copy['NM_MUNICIPIO_IBGE'].str.split(' - ').str[0].str.upper().str.strip()
    df_ibge_copy['UF_LIMPO'] = df_ibge_copy['NM_MUNICIPIO_IBGE'].str.split(' - ').str[1].str.upper().str.strip()
    df_ibge_copy['CHAVE_JOIN'] = df_ibge_copy['NM_LIMPO'] + "_" + df_ibge_copy['UF_LIMPO']
    
    #Prepara a CHAVE_JOIN no TSE usando o mapeamento dinâmico
    df_tse_copy['CHAVE_JOIN'] = df_tse_copy[col_municipio].astype(str).str.upper().str.strip() + "_" + df_tse_copy[col_uf].astype(str).str.upper().str.strip()
    
    #Realiza o merge
    df_resultado = pd.merge(df_tse_copy, df_ibge_copy, on='CHAVE_JOIN', how='inner')
    
    #Cria a feature inteligente se a coluna de aptos existir
    if col_aptos and col_aptos in df_resultado.columns and 'POPULACAO_2022' in df_resultado.columns:
        df_resultado['PROP_ELEITORADO'] = (df_resultado[col_aptos] / df_resultado['POPULACAO_2022']) * 100
    else:
        df_resultado['PROP_ELEITORADO'] = 80.0  # Média nacional de segurança caso o arquivo de treino antigo não tenha QT_APTOS
    
    #Garante que a coluna target tenha o nome correto esperado pela IA
    col_target_original = [c for c in df_resultado.columns if 'PERC' in c or 'DESCONTENTES' in c]
    if col_target_original:
        df_resultado['PERC_DESCONTENTES'] = df_resultado[col_target_original[0]]
        
    #Limpa colunas auxiliares
    df_resultado = df_resultado.drop(columns=['CHAVE_JOIN', 'NM_LIMPO', 'UF_LIMPO'], errors='ignore')
    return df_resultado

#Execução do cruzamento duplo seguro
if os.path.exists(caminho_ibge):
    df_ibge = pd.read_csv(caminho_ibge)
    
    #LIVRO DE ESTUDO (25 Estados)
    if os.path.exists(caminho_treino_tse):
        print("Processando base de TREINO (25 Estados)...")
        df_treino_raw = pd.read_csv(caminho_treino_tse, sep=None, engine='python', encoding='latin-1', on_bad_lines='skip')
        df_treino_final = cruzar_com_ibge(df_treino_raw, df_ibge)
        df_treino_final.to_csv(os.path.join(pasta_dados, 'matriz_treino_25_estados.csv'), index=False, sep=';', encoding='latin-1')
        print(f"[OK] Matriz de TREINO gerada com {df_treino_final.shape[0]} cidades.")
        
    #FOLHA DE PROVA (SP e MG)
    if os.path.exists(caminho_teste_tse):
        print("Processando base de TESTE (SP/MG)...")
        df_teste_raw = pd.read_csv(caminho_teste_tse, sep=None, engine='python', encoding='latin-1', on_bad_lines='skip')
        df_teste_final = cruzar_com_ibge(df_teste_raw, df_ibge)
        df_teste_final.to_csv(os.path.join(pasta_dados, 'matriz_teste_sp_mg.csv'), index=False, sep=';', encoding='latin-1')
        print(f"[OK] Matriz de TESTE CEGO gerada com {df_teste_final.shape[0]} cidades.")
        
    print("\nFase de Engenharia de Dados alinhada e blindada com sucesso!")
else:
    print("Erro: Base do IBGE não encontrada.")