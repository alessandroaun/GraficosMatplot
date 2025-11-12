import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# *** REAPLICAÇÃO DO PIPELINE DE CARREGAMENTO (AJUSTE NECESSÁRIO) ***

caminho_arquivo = r'C:\Users\aless\Documents\GraficosMatplot\df_final_analise_com_capping_IQR2.csv' 

# 1. Carregamento Robusto
try:
    df = pd.read_csv(caminho_arquivo, sep=';', decimal=',', encoding='latin-1')
except Exception:
    df = pd.read_csv(caminho_arquivo, sep=',', encoding='latin-1')


# 2. CONVERSÃO EXPLÍCITA E GARANTIDA PARA FLOAT
def converter_virgula_para_ponto_e_float(serie):
    if serie.dtype == 'object':
        serie_limpa = serie.astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        return pd.to_numeric(serie_limpa, errors='coerce')
    return serie

colunas_para_converter = ['IDH_Valor', 'Preco_m2', 'Renda_Media_Mensal', 'Preco', 'Metros_Quadrados']

for coluna in colunas_para_converter:
    if coluna in df.columns:
        df[coluna] = converter_virgula_para_ponto_e_float(df[coluna])


# --- 3. GERAÇÃO DO GRÁFICO DE BARRAS (Top 10 Bairros por Preço Médio/m²) ---

# Remove linhas sem Bairro ou Preco_m2
df.dropna(subset=['Bairro', 'Preco_m2'], inplace=True)

# Remove valores de preço/m² iguais a zero ou negativos (se houver, mesmo após o capping)
df = df[df['Preco_m2'] > 0].copy() 

# 3.1. Selecionar os 10 bairros com mais anúncios
top_10_bairros = df['Bairro'].value_counts().nlargest(10).index
df_top_10 = df[df['Bairro'].isin(top_10_bairros)].copy()

# 3.2. Calcular a média do Preco_m2 para esses 10 bairros
df_media_bairro = df_top_10.groupby('Bairro')['Preco_m2'].mean().reset_index()

# 3.3. Ordenar os bairros pelo preço médio para o gráfico
df_media_bairro = df_media_bairro.sort_values(by='Preco_m2', ascending=False)

sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 7))

# Gráfico de Barras
sns.barplot(
    x='Bairro', 
    y='Preco_m2', 
    data=df_media_bairro,
    palette='magma'
)

# Função para formatar o eixo Y com o separador de milhar
def formatar_milhar(x, pos):
    return f'R$ {int(x/1000)}K' if x >= 1000 else f'R$ {int(x)}'

plt.title('Preço Médio por m² dos 10 Bairros com Maior Volume de Anúncios', fontsize=14)
plt.xlabel('Bairro', fontsize=12)
plt.ylabel('Preço Médio por m² (R$)', fontsize=12)

# Aplicando a formatação do eixo Y
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(formatar_milhar))

plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout() 
plt.show()