import pandas as pd
import os
import joblib
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, classification_report

print("=== EVOLUÇÃO MÁXIMA DA IA: TREINAMENTO COM CATBOOST COMPLETO ===")

#Caminhos das matrizes
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
pasta_dados = os.path.join(diretorio_atual, 'dados')

caminho_treino = os.path.join(pasta_dados, 'perfil_treino_25_estados.csv')
caminho_teste = os.path.join(pasta_dados, 'perfil_teste_sp_mg.csv')

#Carregamento dos dados 
df_treino = pd.read_csv(caminho_treino, sep=';')
df_teste = pd.read_csv(caminho_teste, sep=';')

y_train = df_treino['VOTO_TERCEIRA_VIA_OU_BRANCO']
y_test = df_teste['VOTO_TERCEIRA_VIA_OU_BRANCO']

#Características brutas
features = ['IDADE', 'ESCOLARIDADE', 'ESTADO', 'MORA_COM_PAIS', 'RECEBE_AUXILIO', 'RELIGIAO']
X_train = df_treino[features].copy()
X_test = df_teste[features].copy()

#Garantimos que as colunas booleanas/numéricas fiquem como inteiros
X_train['MORA_COM_PAIS'] = X_train['MORA_COM_PAIS'].astype(int)
X_train['RECEBE_AUXILIO'] = X_train['RECEBE_AUXILIO'].astype(int)
X_test['MORA_COM_PAIS'] = X_test['MORA_COM_PAIS'].astype(int)
X_test['RECEBE_AUXILIO'] = X_test['RECEBE_AUXILIO'].astype(int)

#Mapeamento de Categoria nativo do CatBoost 
categorical_features_indices = [1, 2, 5]

#Salvamos a lista atualizada de features que o modelo espera no app.py
joblib.dump(features, os.path.join(pasta_dados, 'colunas_modelo.pkl'))

#FASE DE APRENDIZADO COM CATBOOST
print("\n[Passo 1] O CatBoost está processando as categorias nativamente...")
modelo_cat = CatBoostClassifier(
    iterations=150,
    depth=6,
    learning_rate=0.1,
    cat_features=categorical_features_indices,
    auto_class_weights='Balanced', #usando calculo para balancear!
    random_seed=42,
    verbose=0 
)

modelo_cat.fit(X_train, y_train)
print("-> Treinamento com CatBoost concluído!")

#Aplicando a Prova Cega em SP e MG
print("\n[Passo 2] Aplicando a Prova Cega em SP e MG...")
previsoes_gabarito = modelo_cat.predict(X_test)

#Avaliação Real do Desempenho
acuracia = accuracy_score(y_test, previsoes_gabarito)
print("\n================ GABARITO DA AVALIAÇÃO COM CATBOOST ================")
print(f"Nova Acurácia Geral do Agente: {acuracia * 100:.2f}%")
print("====================================================================")
print("\nRelatório Detalhado de Classificação:")
print(classification_report(y_test, previsoes_gabarito, target_names=['Voto em Polos', 'Terceira Via/Branco/Nulo']))

#Salvando o Novo Modelo Atualizado
caminho_export_modelo = os.path.join(pasta_dados, 'modelo_eleitoral.pkl')
joblib.dump(modelo_cat, caminho_export_modelo)
print(f"\n[SUCESSO] O arquivo 'modelo_eleitoral.pkl' foi atualizado com o CatBoost!")