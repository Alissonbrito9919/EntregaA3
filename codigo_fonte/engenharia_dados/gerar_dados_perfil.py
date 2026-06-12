import pandas as pd
import numpy as np
import os

print("Gerando bases de Microdados com Novas Opções Religiosas...")

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
pasta_dados = os.path.join(diretorio_atual, 'dados')
os.makedirs(pasta_dados, exist_ok=True)

def gerar_eleitores(qtd_linhas, estados):
    np.random.seed(42)
    
    idades = np.random.randint(18, 75, size=qtd_linhas)
    
    escolaridades = np.random.choice(
        ['Ensino Fundamental', 'Ensino Médio Incompleto', 'Ensino Médio Completo', 'Ensino Superior'],
        size=qtd_linhas, p=[0.2, 0.2, 0.4, 0.2]
    )
    
    lista_estados = np.random.choice(estados, size=qtd_linhas)
    
    mora_com_pais = []
    recebe_auxilio = []
    

    religioes = np.random.choice(
        ['Católica', 'Evangélica', 'Candomblé', 'Umbanda', 'Sem religião / Ateu', 'Outras'],
        size=qtd_linhas, p=[0.48, 0.30, 0.03, 0.02, 0.13, 0.04]
    )
    
    for i in range(qtd_linhas):
        if idades[i] <= 25:
            mora_com_pais.append(np.random.choice([1, 0], p=[0.7, 0.3]))
        elif idades[i] <= 35:
            mora_com_pais.append(np.random.choice([1, 0], p=[0.3, 0.7]))
        else:
            mora_com_pais.append(np.random.choice([1, 0], p=[0.05, 0.95]))
            
        if escolaridades[i] in ['Ensino Fundamental', 'Ensino Médio Incompleto']:
            recebe_auxilio.append(np.random.choice([1, 0], p=[0.4, 0.6]))
        else:
            recebe_auxilio.append(np.random.choice([1, 0], p=[0.1, 0.9]))

    voto_terceira_via = []
    for i in range(qtd_linhas):
        probabilidade_base = 0.15 
        
        if idades[i] <= 26 and mora_com_pais[i] == 1:
            probabilidade_base += 0.20
            
        if religioes[i] == 'Sem religião / Ateu':
            probabilidade_base += 0.15
        elif religioes[i] == 'Evangélica':
            probabilidade_base -= 0.05
        # Eleitores de matriz africana costumam ter forte engajamento em frentes plurais
        elif religioes[i] in ['Candomblé', 'Umbanda']:
            probabilidade_base += 0.08
            
        if escolaridades[i] == 'Ensino Superior':
            probabilidade_base += 0.10
            
        probabilidade_base = max(0.0, min(1.0, probabilidade_base))
        voto_final = np.random.choice([1, 0], p=[probabilidade_base, 1 - probabilidade_base])
        voto_terceira_via.append(voto_final)

    df = pd.DataFrame({
        'IDADE': idades,
        'ESCOLARIDADE': escolaridades,
        'ESTADO': lista_estados,
        'MORA_COM_PAIS': mora_com_pais,
        'RECEBE_AUXILIO': recebe_auxilio,
        'RELIGIAO': religioes,
        'VOTO_TERCEIRA_VIA_OU_BRANCO': voto_terceira_via
    })
    return df

estados_treino = ['BA', 'RJ', 'CE', 'PE', 'PR', 'RS', 'SC', 'GO', 'AM', 'PA', 'MA', 'PI', 'RN', 'PB', 'AL', 'SE', 'TO', 'RO', 'AC', 'RR', 'AP', 'MS', 'MT', 'ES', 'DF']
df_treino = gerar_eleitores(30000, estados_treino)
df_treino.to_csv(os.path.join(pasta_dados, 'perfil_treino_25_estados.csv'), index=False, sep=';')

estados_teste = ['SP', 'MG']
df_teste = gerar_eleitores(10000, estados_teste)
df_teste.to_csv(os.path.join(pasta_dados, 'perfil_teste_sp_mg.csv'), index=False, sep=';')

print("\n[SUCESSO] Novas bases geradas com Candomblé e Umbanda prontas na pasta 'dados'!")