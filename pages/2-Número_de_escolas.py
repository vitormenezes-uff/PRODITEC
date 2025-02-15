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


# Função para carregar os dados
def load_data():
    return pd.read_csv("consolidado_matriculas.csv")


# Carregar os dados
df = load_data()

# Garantir que a coluna de UF esteja em maiúsculas
if "UF" in df.columns:
    df["UF"] = df["UF"].str.upper()

# Dicionário de mapeamento das UFs para suas respectivas regiões
regioes_map = {
    'AC': 'NORTE', 'AP': 'NORTE', 'AM': 'NORTE', 'PA': 'NORTE', 'RO': 'NORTE', 'RR': 'NORTE', 'TO': 'NORTE',
    'AL': 'NORDESTE', 'BA': 'NORDESTE', 'CE': 'NORDESTE', 'MA': 'NORDESTE', 'PB': 'NORDESTE', 'PE': 'NORDESTE',
    'PI': 'NORDESTE', 'RN': 'NORDESTE', 'SE': 'NORDESTE',
    'DF': 'CENTRO-OESTE', 'GO': 'CENTRO-OESTE', 'MT': 'CENTRO-OESTE', 'MS': 'CENTRO-OESTE',
    'ES': 'SUDESTE', 'MG': 'SUDESTE', 'RJ': 'SUDESTE', 'SP': 'SUDESTE',
    'PR': 'SUL', 'RS': 'SUL', 'SC': 'SUL'
}
df["REGIAO"] = df["UF"].map(regioes_map)

# Criar abas
aba_municipios, aba_estados, aba_regioes, aba_pizza = st.tabs(
    ["Escolas por Município", "Escolas por Estado", "Escolas por Região", "Distribuição"])

with aba_municipios:
    st.title("Quantidade de Escolas por Município")
    uf_selecionada = st.selectbox("Selecione uma UF:", sorted(df["UF"].unique()))
    df_municipios = df[df["UF"] == uf_selecionada]
    municipios_counts = df_municipios["NOME MUNICÍPIO"].value_counts().reset_index()
    municipios_counts.columns = ["Município", "Quantidade"]
    fig_municipios = px.bar(municipios_counts, x="Município", y="Quantidade",
                            title=f"Quantidade de Escolas por Município em {uf_selecionada}")
    st.plotly_chart(fig_municipios)

with aba_estados:
    st.title("Quantidade de Escolas por Estado")
    regiao_selecionada = st.selectbox("Selecione uma Região:", sorted(df["REGIAO"].dropna().unique()))
    df_estados = df[df["REGIAO"] == regiao_selecionada]
    estados_counts = df_estados["UF"].value_counts().reset_index()
    estados_counts.columns = ["UF", "Quantidade"]
    fig_estados = px.bar(estados_counts, x="UF", y="Quantidade",
                         title=f"Quantidade de Escolas por Estado na Região {regiao_selecionada}")
    st.plotly_chart(fig_estados)

with aba_regioes:
    st.title("Quantidade de Escolas por Região")
    regioes_counts = df["REGIAO"].value_counts().reset_index()
    regioes_counts.columns = ["Região", "Quantidade"]
    fig_regioes = px.bar(regioes_counts, x="Região", y="Quantidade",
                         title="Quantidade de Escolas por Região")
    st.plotly_chart(fig_regioes)

with aba_pizza:
    st.title("Distribuição das Escolas no Brasil")

    # Gráfico de pizza para distribuição nacional
    fig_pizza_nacional = px.pie(regioes_counts, names="Região", values="Quantidade",
                                title="Distribuição de Escolas pelo Brasil (por Região)")
    st.plotly_chart(fig_pizza_nacional)

    # Dropdown para seleção de região
    regiao_pizza = st.selectbox("Selecione uma Região para ver a distribuição por Estado:",
                                sorted(df["REGIAO"].dropna().unique()))
    df_pizza_estados = df[df["REGIAO"] == regiao_pizza]
    estados_pizza_counts = df_pizza_estados["UF"].value_counts().reset_index()
    estados_pizza_counts.columns = ["UF", "Quantidade"]
    fig_pizza_estados = px.pie(estados_pizza_counts, names="UF", values="Quantidade",
                               title=f"Distribuição de Escolas na Região {regiao_pizza} (por Estado)")
    st.plotly_chart(fig_pizza_estados)

    # Dropdown para seleção de estado
    estado_pizza = st.selectbox("Selecione um Estado para ver a distribuição por Município:", sorted(df["UF"].unique()))
    df_pizza_municipios = df[df["UF"] == estado_pizza]
    municipios_pizza_counts = df_pizza_municipios["NOME MUNICÍPIO"].value_counts().reset_index()
    municipios_pizza_counts.columns = ["Município", "Quantidade"]
    fig_pizza_municipios = px.pie(municipios_pizza_counts, names="Município", values="Quantidade",
                                  title=f"Distribuição de Escolas no Estado {estado_pizza} (por Município)")
    st.plotly_chart(fig_pizza_municipios)
