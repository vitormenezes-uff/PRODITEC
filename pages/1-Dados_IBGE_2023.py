import streamlit as st
import pandas as pd
import plotly.express as px
import os
from config_pagina import configurar_pagina  # Importa a configuração da página

# Obtém o nome do arquivo atual dinamicamente
nome_arquivo = os.path.basename(__file__)

# Configura a página automaticamente
configurar_pagina(nome_arquivo)

# Carregar os dados (substituir pelo caminho real do arquivo)
@st.cache_data
def load_data():
    return pd.read_csv("consolidado_matriculas.csv")

df = load_data()

# Excluir colunas indesejadas
colunas_excluir = [
    'POSSUI INTERNET', 'INTERNET BANDA LARGA', 'PROF MONITORES', 'AEE', 'ATIVIDADE COMPLEMENTAR',
    'ESCOLARIZACAO', 'ENSINO INFANTIL', 'ENSINO FUNDAMENTAL', 'ENSINO MÉDIO', 'ENSINO PROFISIONALIZANTE',
    'EJA', 'EDUCAÇÃO ESPECIAL', 'ENSINO TÉC. PROF.'
]
df.drop(columns=colunas_excluir, inplace=True, errors='ignore')

# Ordenar os dados para evitar problemas de visualização
df.sort_values(by=['UF', 'NOME MUNICÍPIO'], inplace=True)

# Criar abas
aba_graficos, aba_tabelas = st.tabs(["Gráficos", "Tabelas"])

with aba_graficos:
    st.title("Análise de distribuição de Matrículas pelas Unidades Escolares agregadas por UF")

    # Gráfico boxplot por UF
    fig = px.box(df, x='UF', y='QTDE MATRÍCULAS', title="Distribuição de Matrículas por UF",
                 hover_data=['NOME MUNICÍPIO'], category_orders={'UF': sorted(df['UF'].unique())})
    st.plotly_chart(fig, use_container_width=True, key="boxplot_uf")

    # Removendo outliers corretamente por UF
    def remover_outliers_por_uf(grupo):
        q1 = grupo['QTDE MATRÍCULAS'].quantile(0.25)
        q3 = grupo['QTDE MATRÍCULAS'].quantile(0.75)
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        return grupo[(grupo['QTDE MATRÍCULAS'] >= limite_inferior) & (grupo['QTDE MATRÍCULAS'] <= limite_superior)]

    df_filtrado = df.groupby("UF", group_keys=False).apply(remover_outliers_por_uf)

    fig_filtrado = px.box(df_filtrado, x='UF', y='QTDE MATRÍCULAS',
                          title="Distribuição de Matrículas por UF (Sem Outliers)",
                          hover_data=['NOME MUNICÍPIO'],
                          category_orders={'UF': sorted(df['UF'].unique())},
                          points=False)  # Remove a exibição de outliers
    st.plotly_chart(fig_filtrado, use_container_width=True, key="boxplot_uf_sem_outliers")

    # Selecionar UF para detalhamento
    uf_selecionada = st.selectbox("Selecione uma UF para ver os dados por município:", sorted(df['UF'].unique()))

    # Filtrar apenas os dados da UF selecionada
    df_municipios = df[df['UF'] == uf_selecionada].copy()

    # Criar boxplot com todos os dados para a UF selecionada
    fig = px.box(df_municipios, x='NOME MUNICÍPIO', y='QTDE MATRÍCULAS',
                 title=f"Distribuição de Matrículas nos Municípios de {uf_selecionada}",
                 hover_data=['NOME MUNICÍPIO'],
                 category_orders={'NOME MUNICÍPIO': sorted(df_municipios['NOME MUNICÍPIO'].unique())})
    st.plotly_chart(fig, use_container_width=True, key=f"boxplot_municipios_{uf_selecionada}")

    # Garantir que os quartis sejam calculados apenas com os dados da UF selecionada
    df_municipios = df[df['UF'] == uf_selecionada].copy()

    # Calcular Q1, Q3 e IQR apenas para a UF selecionada
    q1 = df_municipios['QTDE MATRÍCULAS'].quantile(0.25)
    q3 = df_municipios['QTDE MATRÍCULAS'].quantile(0.75)
    iqr = q3 - q1

    # Definir os limites das cercas para remoção de outliers
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    # Aplicar a filtragem ANTES de passar para o gráfico
    df_municipios_filtrado = df_municipios[
        (df_municipios['QTDE MATRÍCULAS'] >= limite_inferior) &
        (df_municipios['QTDE MATRÍCULAS'] <= limite_superior)
        ].copy()  # Criar cópia para evitar problemas de referência

    # Criar o gráfico SEM outliers
    fig_municipios_filtrado = px.box(
        df_municipios_filtrado,
        x='NOME MUNICÍPIO',
        y='QTDE MATRÍCULAS',
        title=f"Distribuição de Matrículas nos Municípios de {uf_selecionada} (Sem Outliers)",
        hover_data=['NOME MUNICÍPIO'],
        category_orders={'NOME MUNICÍPIO': sorted(df_municipios_filtrado['NOME MUNICÍPIO'].unique())},
        points=False  # REMOVE explicitamente a exibição de outliers
    )

    # Exibir o gráfico sem outliers
    st.plotly_chart(fig_municipios_filtrado, use_container_width=True,
                    key=f"boxplot_municipios_sem_outliers_{uf_selecionada}")

with aba_tabelas:
    st.title("Tabelas de Dados")
    st.subheader("Dados por UF")
