import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# *** ATENÇÃO: VERIFIQUE NOVAMENTE O CAMINHO EXATO DO ARQUIVO ***
caminho_arquivo = r'C:\Users\aless\Documents\GraficosMatplot\df_final_analise_sem_outliers_IQR.csv' 

# --- 1. CARREGAMENTO E PRÉ-PROCESSAMENTO DE DADOS (ROBUSTO) ---

# Tenta carregar no formato brasileiro: sep=';', decimal=',', e encoding='latin-1'
try:
    # Tenta a combinação mais provável para o seu caso
    df = pd.read_csv(caminho_arquivo, sep=';', decimal=',', encoding='latin-1')
    print("Sucesso no carregamento com separador ';', decimal ',' e encoding 'latin-1'.")
    
except Exception as e:
    # Se falhar, tenta o carregamento com a vírgula como separador e faz a conversão manual
    print(f"Falha na primeira tentativa de leitura. Tentando com separador ',' e conversão manual... (Erro: {e})")
    
    # Tentativa alternativa: sep=',', encoding='latin-1'
    df = pd.read_csv(caminho_arquivo, sep=',', encoding='latin-1')
    
    # Função de conversão manual de números com vírgula para ponto e float
    def converter_virgula_para_ponto_e_float(serie):
        if serie.dtype == 'object':
            # Remove o ponto de milhar, substitui vírgula decimal por ponto, e converte para float
            return serie.astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float, errors='coerce')
        return serie

    # Lista de colunas numéricas a serem tratadas
    colunas_para_converter = ['IDH_Valor', 'Preco_m2', 'Renda_Media_Mensal', 'Preco', 'Metros_Quadrados', 
                              'Condicoes_Ambientais_Urbanas', 'Condicoes_Habitacionais_Urbanas']
    
    for coluna in colunas_para_converter:
        if coluna in df.columns:
            df[coluna] = converter_virgula_para_ponto_e_float(df[coluna])


# --- 2. GERAÇÃO DO GRÁFICO DE CAIXA (BOX PLOT) ---

# Limpeza de dados faltantes nas colunas chave
df.dropna(subset=['Preco_m2', 'Classificacao_IDH'], inplace=True)

sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 7))

# Ordem lógica das categorias de IDH para o gráfico
ordem_idh = sorted(df['Classificacao_IDH'].dropna().unique())

# Gráfico de Caixa (Box Plot)
sns.boxplot(
    x='Classificacao_IDH', 
    y='Preco_m2', 
    data=df,
    order=ordem_idh,
    palette='viridis' 
)

plt.title('Distribuição do Preço por m² por Categoria de IDH em Fortaleza', fontsize=14)
plt.xlabel('Classificação IDH', fontsize=12)
plt.ylabel('Preço por m² (R$)', fontsize=12)
plt.xticks(rotation=15)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout() 
plt.show()