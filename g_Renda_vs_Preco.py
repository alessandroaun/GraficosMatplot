import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# *** REAPLICAÇÃO DO PIPELINE DE CARREGAMENTO ***

# Caminho do arquivo
caminho_arquivo = r'C:\Users\aless\Documents\GraficosMatplot\df_final_analise_com_capping_IQR2.csv' 

# 1. Carregamento Robusto (mantendo o encoding e o fallback de separador)
try:
    df = pd.read_csv(caminho_arquivo, sep=';', decimal=',', encoding='latin-1')
except Exception:
    df = pd.read_csv(caminho_arquivo, sep=',', encoding='latin-1')


# 2. CONVERSÃO EXPLÍCITA E GARANTIDA PARA FLOAT (CORREÇÃO DO ValueError)
def converter_virgula_para_ponto_e_float(serie):
    if serie.dtype == 'object':
        # 1. Limpa a string (remove ponto de milhar, substitui vírgula por ponto decimal)
        serie_limpa = serie.astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        
        # 2. USA pd.to_numeric() para garantir a conversão para float
        return pd.to_numeric(serie_limpa, errors='coerce')
    return serie

colunas_para_converter = ['IDH_Valor', 'Preco_m2', 'Renda_Media_Mensal', 'Preco', 'Metros_Quadrados', 
                          'Condicoes_Ambientais_Urbanas', 'Condicoes_Habitacionais_Urbanas']

for coluna in colunas_para_converter:
    if coluna in df.columns:
        df[coluna] = converter_virgula_para_ponto_e_float(df[coluna])


# --- 3. GERAÇÃO DO GRÁFICO HEXBIN (DENSIDADE) ---

# O DataFrame 'df' é usado diretamente, pois os outliers já foram tratados no CSV original.
df.dropna(subset=['Renda_Media_Mensal', 'Preco_m2'], inplace=True)

sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 7))

# Criação do Hexbin Plot:
plt.hexbin(
    x=df['Renda_Media_Mensal'], # USANDO DF ORIGINAL
    y=df['Preco_m2'], # USANDO DF ORIGINAL
    gridsize=25, 
    cmap='viridis', 
    mincnt=1
)

cb = plt.colorbar(label='Contagem de Anúncios') 

# Função para formatar o eixo Y com o separador de milhar
def formatar_milhar(x, pos):
    return f'R$ {int(x/1000)}K' if x >= 1000 else f'R$ {int(x)}'

plt.title('Densidade da Relação: Renda Média Mensal vs. Preço por m² (Hexbin)', fontsize=14)
plt.xlabel('Renda Média Mensal do Bairro (R$)', fontsize=12)
plt.ylabel('Preço por m² (R$)', fontsize=12)

# Aplicando a formatação do eixo Y
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(formatar_milhar))

plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout() 
plt.show()