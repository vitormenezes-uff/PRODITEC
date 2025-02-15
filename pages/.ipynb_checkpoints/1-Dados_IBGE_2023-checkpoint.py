import streamlit as st
import pandas as pd
import plotly.express as px


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

# Agrupar os dados por UF e calcular estatísticas
dados_uf = df.groupby('UF').agg({'QTDE MATRÍCULAS': ['sum', 'mean', 'median', 'std', 'min', 'max',
                                                     lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]})
dados_uf.columns = ['TOTAL', 'MEDIA', 'MEDIANA', 'STD', 'MIN', 'MAX', 'Q25', 'Q75']
dados_uf.reset_index(inplace=True)

df.sort_values(by=['UF', 'NOME MUNICÍPIO'], inplace=True)

# Criar abas
aba_graficos, aba_tabelas = st.tabs(["Gráficos", "Tabelas"])

with aba_graficos:
    st.title("Análise de distribuição de Matrículas pelas Unidades Escolares agregadas por UF")

    # Gráfico boxplot interativo por UF com nome do município no popup
    fig = px.box(df, x='UF', y='QTDE MATRÍCULAS', title="Distribuição de Matrículas por UF",
                 hover_data=['NOME MUNICÍPIO'], category_orders={'UF': sorted(df['UF'].unique())})
    st.plotly_chart(fig)

    # Removendo outliers utilizando os quartis
    df_filtrado = df[(df['QTDE MATRÍCULAS'] >= df['QTDE MATRÍCULAS'].quantile(0.25)) & (
                df['QTDE MATRÍCULAS'] <= df['QTDE MATRÍCULAS'].quantile(0.75))]
    fig_filtrado = px.box(df_filtrado, x='UF', y='QTDE MATRÍCULAS',
                          title="Distribuição de Matrículas por UF (Sem Outliers)", hover_data=['NOME MUNICÍPIO'],
                          category_orders={'UF': sorted(df['UF'].unique())})
    st.plotly_chart(fig_filtrado)

    # Selecionar UF para detalhamento
    uf_selecionada = st.selectbox("Selecione uma UF para ver os dados por município:", sorted(dados_uf['UF'].unique()))

    # Gráfico boxplot interativo por município
    fig = px.box(df[df['UF'] == uf_selecionada], x='NOME MUNICÍPIO', y='QTDE MATRÍCULAS',
                 title=f"Distribuição de Matrículas nos Municípios de {uf_selecionada}", hover_data=['NOME MUNICÍPIO'],
                 category_orders={'NOME MUNICÍPIO': sorted(df[df['UF'] == uf_selecionada]['NOME MUNICÍPIO'].unique())})
    st.plotly_chart(fig)

    # Removendo outliers do gráfico por município
    df_municipios_filtrado = df[
        (df['UF'] == uf_selecionada) & (df['QTDE MATRÍCULAS'] >= df['QTDE MATRÍCULAS'].quantile(0.25)) & (
                    df['QTDE MATRÍCULAS'] <= df['QTDE MATRÍCULAS'].quantile(0.75))]
    fig_municipios_filtrado = px.box(df_municipios_filtrado, x='NOME MUNICÍPIO', y='QTDE MATRÍCULAS',
                                     title=f"Distribuição de Matrículas nos Municípios de {uf_selecionada} (Sem Outliers)",
                                     hover_data=['NOME MUNICÍPIO'], category_orders={
            'NOME MUNICÍPIO': sorted(df_municipios_filtrado['NOME MUNICÍPIO'].unique())})
    st.plotly_chart(fig_municipios_filtrado)

with aba_tabelas:
    st.title("Tabelas de Dados")
    st.subheader("Dados por UF")
    st.dataframe(dados_uf)

    st.subheader("Dados por Município")
    uf_tabela_selecionada = st.selectbox("Selecione uma UF para ver os dados da tabela por município:",
                                         sorted(dados_uf['UF'].unique()), key="uf_tabelas")

    # Filtrar dados por município dentro da UF selecionada
    dados_municipios = df[df['UF'] == uf_tabela_selecionada].groupby('NOME MUNICÍPIO').agg({'QTDE MATRÍCULAS': ['sum',
                                                                                                                'mean',
                                                                                                                'median',
                                                                                                                'std',
                                                                                                                'min',
                                                                                                                'max',
                                                                                                                lambda
                                                                                                                    x: x.quantile(
                                                                                                                    0.25),
                                                                                                                lambda
                                                                                                                    x: x.quantile(
                                                                                                                    0.75)]})
    dados_municipios.columns = ['TOTAL', 'MEDIA', 'MEDIANA', 'STD', 'MIN', 'MAX', 'Q25', 'Q75']
    dados_municipios.reset_index(inplace=True)
    dados_municipios.sort_values(by='NOME MUNICÍPIO', inplace=True)
    st.dataframe(dados_municipios)