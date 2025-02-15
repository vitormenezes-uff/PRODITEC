import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Obtém o caminho absoluto do diretório raiz do projeto
dir_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Adiciona o diretório raiz ao sys.path para que possamos importar config_pagina.py
if dir_raiz not in sys.path:
    sys.path.append(dir_raiz)

# Agora importa corretamente a função configurar_pagina
from config_pagina import configurar_pagina

# Obtém o nome do arquivo atual dinamicamente
nome_arquivo = os.path.basename(__file__)

# Configura a página automaticamente
configurar_pagina(nome_arquivo)


# Função para carregar os dados do IBGE
@st.cache_data
def load_ibge_data():
    return pd.read_csv("consolidado_matriculas.csv")


# Função para carregar os dados de 2024
@st.cache_data
def load_2024_data():
    return pd.read_csv("dados_2024.csv")


# Carregar os dados
df_ibge = load_ibge_data()
df_2024 = load_2024_data()

# Garantir que a coluna de município esteja padronizada
if "NOME MUNICÍPIO" in df_ibge.columns and "MUNICÍPIO" in df_2024.columns:
    df_2024.rename(columns={"MUNICÍPIO": "NOME MUNICÍPIO"}, inplace=True)

# Dicionário de mapeamento das UFs para suas respectivas regiões
regioes_map = {
    'AC': 'NORTE', 'AP': 'NORTE', 'AM': 'NORTE', 'PA': 'NORTE', 'RO': 'NORTE', 'RR': 'NORTE', 'TO': 'NORTE',
    'AL': 'NORDESTE', 'BA': 'NORDESTE', 'CE': 'NORDESTE', 'MA': 'NORDESTE', 'PB': 'NORDESTE', 'PE': 'NORDESTE',
    'PI': 'NORDESTE', 'RN': 'NORDESTE', 'SE': 'NORDESTE',
    'DF': 'CENTRO-OESTE', 'GO': 'CENTRO-OESTE', 'MT': 'CENTRO-OESTE', 'MS': 'CENTRO-OESTE',
    'ES': 'SUDESTE', 'MG': 'SUDESTE', 'RJ': 'SUDESTE', 'SP': 'SUDESTE',
    'PR': 'SUL', 'RS': 'SUL', 'SC': 'SUL'
}
df_ibge["REGIAO"] = df_ibge["UF"].map(regioes_map)

# Filtrar os municípios atendidos no df_2024
df_ibge_filtrado = df_ibge[df_ibge["NOME MUNICÍPIO"].isin(df_2024["NOME MUNICÍPIO"].unique())]

# Criar abas
abas_graficos20242, aba_tabelas20242 = st.tabs(["Gráficos - 2024/2", "Tabelas - 2024/2"])

with abas_graficos20242:
    st.title("Distribuição de Matrículas por Região, Estado e Município - 2024")

    # Gráfico boxplot por Região
    fig_regiao = px.box(df_ibge_filtrado, x='REGIAO', y='QTDE MATRÍCULAS',
                        title="Distribuição de Matrículas por Região",
                        hover_data=['NOME MUNICÍPIO', 'UF'])
    st.plotly_chart(fig_regiao)

    # Gráfico boxplot por Região sem outliers
    df_regiao_sem_outliers = df_ibge_filtrado[
        (df_ibge_filtrado['QTDE MATRÍCULAS'] >= df_ibge_filtrado['QTDE MATRÍCULAS'].quantile(0.25)) &
        (df_ibge_filtrado['QTDE MATRÍCULAS'] <= df_ibge_filtrado['QTDE MATRÍCULAS'].quantile(0.75))
        ]
    fig_regiao_sem_outliers = px.box(df_regiao_sem_outliers, x='REGIAO', y='QTDE MATRÍCULAS',
                                     title="Distribuição de Matrículas por Região (Sem Outliers)",
                                     hover_data=['NOME MUNICÍPIO', 'UF'])
    st.plotly_chart(fig_regiao_sem_outliers)

    # Dropdown para seleção de Região
    regiao_selecionada = st.selectbox("Selecione uma Região para ver os dados por Estado:",
                                      sorted(df_ibge_filtrado['REGIAO'].unique()))

    # Filtrando por região e criando gráficos por Estado
    df_estados = df_ibge_filtrado[df_ibge_filtrado['REGIAO'] == regiao_selecionada]
    fig_estado = px.box(df_estados, x='UF', y='QTDE MATRÍCULAS',
                        title=f"Distribuição de Matrículas por Estado na Região {regiao_selecionada}",
                        hover_data=['NOME MUNICÍPIO'])
    st.plotly_chart(fig_estado)

    df_estados_sem_outliers = df_estados[
        (df_estados['QTDE MATRÍCULAS'] >= df_estados['QTDE MATRÍCULAS'].quantile(0.25)) &
        (df_estados['QTDE MATRÍCULAS'] <= df_estados['QTDE MATRÍCULAS'].quantile(0.75))
        ]
    fig_estado_sem_outliers = px.box(df_estados_sem_outliers, x='UF', y='QTDE MATRÍCULAS',
                                     title=f"Distribuição de Matrículas por Estado na Região {regiao_selecionada} (Sem Outliers)",
                                     hover_data=['NOME MUNICÍPIO'])
    st.plotly_chart(fig_estado_sem_outliers)

    # Dropdown para seleção de UF
    uf_selecionada = st.selectbox("Selecione uma UF para ver os dados por município:",
                                  sorted(df_estados['UF'].unique()))

    # Filtrando por UF e criando gráficos por Município
    df_municipios = df_estados[df_estados['UF'] == uf_selecionada]
    fig_municipios = px.box(df_municipios, x='NOME MUNICÍPIO', y='QTDE MATRÍCULAS',
                            title=f"Distribuição de Matrículas nos Municípios de {uf_selecionada}",
                            hover_data=['NOME MUNICÍPIO'])
    st.plotly_chart(fig_municipios)

    df_municipios_sem_outliers = df_municipios[
        (df_municipios['QTDE MATRÍCULAS'] >= df_municipios['QTDE MATRÍCULAS'].quantile(0.25)) &
        (df_municipios['QTDE MATRÍCULAS'] <= df_municipios['QTDE MATRÍCULAS'].quantile(0.75))
        ]
    fig_municipios_sem_outliers = px.box(df_municipios_sem_outliers, x='NOME MUNICÍPIO', y='QTDE MATRÍCULAS',
                                         title=f"Distribuição de Matrículas nos Municípios de {uf_selecionada} (Sem Outliers)",
                                         hover_data=['NOME MUNICÍPIO'])
    st.plotly_chart(fig_municipios_sem_outliers)

with aba_tabelas20242:
    st.title("Tabelas de Dados")
    st.subheader("Dados por Região")
    st.dataframe(
        df_ibge_filtrado.groupby('REGIAO').agg({'QTDE MATRÍCULAS': ['sum', 'mean', 'median', 'std', 'min', 'max']}))

    st.subheader("Dados por UF")
    st.dataframe(
        df_ibge_filtrado.groupby('UF').agg({'QTDE MATRÍCULAS': ['sum', 'mean', 'median', 'std', 'min', 'max']}))
