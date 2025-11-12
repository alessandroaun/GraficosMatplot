import pandas as pd
import numpy as np

# 1. Carregar o arquivo com o encoding correto
try:
    df = pd.read_csv('df_final_analise_por_anuncio.csv', sep=';', encoding='latin-1')
except UnicodeDecodeError:
    # Tentar outro encoding comum se latin-1 falhar
    df = pd.read_csv('df_final_analise_por_anuncio.csv', sep=';', encoding='cp1252')

# Garantir que 'Preco_m2' é numérica
df['Preco_m2'] = pd.to_numeric(df['Preco_m2'], errors='coerce')

# --- CONFIGURAÇÃO DO NOVO TRATAMENTO ---
FATOR_IQR = 2.0
# ---

# 2. Calcular Q1, Q3 e IQR para a coluna 'Preco_m2'
Q1 = df['Preco_m2'].quantile(0.25)
Q3 = df['Preco_m2'].quantile(0.75)
IQR = Q3 - Q1

# 3. Definir o novo limite superior
# Usando FATOR_IQR = 2.0 para ser mais permissivo
limite_superior = Q3 + FATOR_IQR * IQR
# O limite inferior (para preços) é sempre 0
limite_inferior = max(0, Q1 - FATOR_IQR * IQR)

print(f"--- NOVOS LIMITES (Fator {FATOR_IQR}) ---")
print(f"Q1: {Q1:,.2f} | Q3: {Q3:,.2f}")
print(f"Novo Limite Superior: R$ {limite_superior:,.2f}")

# 4. Aplicar a Limitação (Capping)
# Substituir todos os valores ACIMA do limite superior pelo próprio limite superior
df['Preco_m2_Tratado'] = np.where(
    df['Preco_m2'] > limite_superior,
    limite_superior,
    df['Preco_m2']
)

# Opcional: Substituir valores ABAIXO do limite inferior (se houver e for relevante)
df['Preco_m2_Tratado'] = np.where(
    df['Preco_m2_Tratado'] < limite_inferior,
    limite_inferior,
    df['Preco_m2_Tratado']
)

# 5. Criar o DataFrame final apenas com as colunas relevantes
df_final = df.drop(columns=['Preco_m2']).rename(columns={'Preco_m2_Tratado': 'Preco_m2'})
df_final = df_final[df.columns[:-1]] # Reordena as colunas para o formato original

# 6. Salvar o DataFrame tratado em um novo arquivo CSV
nome_do_arquivo = 'df_final_analise_com_capping_IQR2.csv'
df_final.to_csv(nome_do_arquivo, sep=';', index=False)

print("\n--- RESULTADO ---")
print(f"Número de linhas ANTES/DEPOIS: {len(df_final)} / {len(df_final)} (Não houve redução!)")
print(f"Valores ajustados (Capping) no Limite Superior: {len(df[df['Preco_m2'] > limite_superior])}")
print(f"✅ Tratamento de CAPPING concluído! O novo arquivo CSV '{nome_do_arquivo}' foi salvo.")