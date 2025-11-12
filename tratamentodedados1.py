import pandas as pd

# 1. Carregar o arquivo com o encoding correto (latin-1)
# Agora deve funcionar, pois resolvemos o erro de decodificação.
df = pd.read_csv('df_final_analise_por_anuncio.csv', sep=';', encoding='latin-1')

# --- O RESTANTE DO TRATAMENTO DE OUTLIERS ---

# Garantir que a coluna 'Preco_m2' é numérica (caso houvesse problemas de leitura com a vírgula, mas no seu caso o separador é ';', então deve estar ok)
df['Preco_m2'] = pd.to_numeric(df['Preco_m2'], errors='coerce')

# 2. Calcular Q1, Q3 e IQR para a coluna 'Preco_m2'
Q1 = df['Preco_m2'].quantile(0.25)
Q3 = df['Preco_m2'].quantile(0.75)
IQR = Q3 - Q1

# 3. Definir os limites de remoção de outliers (1.5 * IQR)
limite_inferior = max(0, Q1 - 1.5 * IQR)
limite_superior = Q3 + 1.5 * IQR

# 4. Filtrar o DataFrame para remover os outliers
df_tratado = df[
    (df['Preco_m2'] >= limite_inferior) &
    (df['Preco_m2'] <= limite_superior)
]

# 5. Salvar o DataFrame tratado em um novo arquivo CSV
nome_do_arquivo = 'df_final_analise_sem_outliers_IQR.csv'
df_tratado.to_csv(nome_do_arquivo, sep=';', index=False)

print(f"✅ Sucesso! O novo arquivo CSV '{nome_do_arquivo}' foi salvo com os outliers de Preco_m2 removidos.")