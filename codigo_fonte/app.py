import os
import joblib
import pandas as pd

def carregar_modelo_e_features():
    """Carrega o modelo CatBoost e a lista de colunas usando caminhos relativos robustos."""
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_dados = os.path.join(diretorio_atual, 'dados')
    caminho_modelo = os.path.join(pasta_dados, 'modelo_eleitoral.pkl')
    caminho_colunas = os.path.join(pasta_dados, 'colunas_modelo.pkl')

    if os.path.exists(caminho_modelo) and os.path.exists(caminho_colunas):
        modelo = joblib.load(caminho_modelo)
        features = joblib.load(caminho_colunas)
        return modelo, features
    return None, None

def rodar_agente_terminal():
    print("\n" + "="*65)
    print("AGENTE SECRETO DE IA: CLASSIFICAÇÃO DE PERFIL ELEITORAL ")
    print("="*65)


    #Carrega a base de dados
    modelo, features = carregar_modelo_e_features()
    if modelo is None:
        print("\n[ERRO] Não foi possível carregar os arquivos do modelo na pasta 'dados'!")
        return

    print("\nPor favor, informe os dados demográficos para análise:\n")
    
    #Idade
    while True:
        try:
            idade = int(input("1. Qual é a idade? (De 18 a 80): "))
            if 18 <= idade <= 80:
                break
            print("Idade inválida. Digite um valor entre 18 e 80.")
        except ValueError:
            print("Entrada inválida. Digite apenas números inteiros.")

    #Escolaridade 
    print("\n2. Qual o grau de escolaridade?")
    opcoes_escola = [
        "Ensino Fundamental Incompleto",
        "Ensino Fundamental Completo",
        "Ensino Médio Incompleto",
        "Ensino Médio Completo",
        "Ensino Superior Incompleto",
        "Ensino Superior Completo"
    ]
    for i, opcao in enumerate(opcoes_escola, 1):
        print(f"  [{i}] {opcao}")
    while True:
        try:
            idx = int(input("Escolha uma opção (1 a 6): ")) - 1  # Ajustado limite máximo para 6
            if 0 <= idx < len(opcoes_escola):
                escolaridade = opcoes_escola[idx]
                break
        except ValueError:
            pass
        print("Opção inválida. Digite um número de 1 a 6.")

    #Estado
    estado = input("\n3. Qual a sigla do Estado? (Ex: BA, SP, MG): ").strip().upper()

    #Mora com os pais
    print("\n4. Reside atualmente com os pais?")
    print("  [1] Sim\n  [2] Não")
    mora_com_pais = 1 if input("Escolha (1 ou 2): ").strip() == "1" else 0

    #Recebe auxílio
    print("\n5. Recebe algum auxílio financeiro governamental?")
    print("  [1] Sim\n  [2] Não")
    recebe_auxilio = 1 if input("Escolha (1 ou 2): ").strip() == "1" else 0

    #Religião
    print("\n6. Qual é a filiação religiosa?")
    opcoes_religiao = ["Católica", "Evangélica", "Candomblé", "Umbanda", "Sem religião / Ateu", "Outras"]
    for i, opcao in enumerate(opcoes_religiao, 1):
        print(f"  [{i}] {opcao}")
    while True:
        try:
            idx = int(input("Escolha uma opção (1 a 6): ")) - 1
            if 0 <= idx < len(opcoes_religiao):
                religiao = opcoes_religiao[idx]
                break
        except ValueError:
            pass
        print("Opção inválida. Digite um número de 1 a 6.")

    print("\n" + "."*40)
    print("O Agente secreto  está processando as variáveis...")
    print("."*40)
    
    # 2. Construção da Matriz de Entrada (ESTADO incluído com sucesso)
    dados = pd.DataFrame([{
        'IDADE': int(idade),
        'ESCOLARIDADE': str(escolaridade),
        'ESTADO': str(estado), 
        'MORA_COM_PAIS': int(mora_com_pais),
        'RECEBE_AUXILIO': int(recebe_auxilio),
        'RELIGIAO': str(religiao)
    }])
    
    #Ordenação estrita baseada nas colunas mapeadas pelo pkl
    dados = dados[features]
    
    #Predição de Probabilidades
    probabilidades = modelo.predict_proba(dados)[0]
    prob_polos = probabilidades[0] * 100
    prob_terceira = probabilidades[1] * 100

    #Painel de Resultados Textual
    print("\n=================== GABARITO DE ANÁLISE ===================")
    print(f"Propensão ao Alinhamento de Polos:     {prob_polos:.2f}%")
    print(f"Propensão a Alternativos/Branco/Nulo:  {prob_terceira:.2f}%")
    print("===========================================================")
    
if __name__ == "__main__":
    rodar_agente_terminal()