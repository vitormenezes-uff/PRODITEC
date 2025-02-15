#===

import pandas as pd
import plotly.express as px
import streamlit as st
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


#=========================#
#       PROCESSAMENTO     #
#=========================#

# Carregar os dados do Censo Escolar e do PRODITEC 2024
censo_escolar = pd.read_csv("consolidado_matriculas.csv")
dados_2024 = pd.read_csv("dados_2024.csv")

# Renomear a coluna "SIGLA UF" para "UF" (se necessário)
censo_escolar = censo_escolar.rename(columns={"SIGLA UF": "UF"})
dados_2024 = dados_2024.rename(columns={"SIGLA UF": "UF"})

# Criar identificador único para municípios, combinando "UF" e "NOME MUNICÍPIO"
censo_escolar["ID_MUNICIPIO"] = censo_escolar["UF"] + " - " + censo_escolar["NOME MUNICÍPIO"]
dados_2024["ID_MUNICIPIO"] = dados_2024["UF"] + " - " + dados_2024["NOME MUNICÍPIO"]

# Contar o número total de escolas por município
numero_escolas_municipio = censo_escolar.groupby("ID_MUNICIPIO").size().reset_index(name="QT_ESCOLAS")

# Associar os diretores/técnicos ao número total de escolas do município
dados_2024 = dados_2024.merge(numero_escolas_municipio, on="ID_MUNICIPIO", how="left")

# Criar 10 grupos equilibrados usando `qcut`, garantindo faixas numéricas reais
intervalos = pd.qcut(dados_2024["QT_ESCOLAS"], q=10, retbins=True, duplicates="drop")[1]
dados_2024["CATEGORIA_QT_ESCOLAS"] = pd.cut(dados_2024["QT_ESCOLAS"], bins=intervalos, include_lowest=True)

# Criar coluna de evasão: 1 para evadido, 0 para concluído
dados_2024["EVASAO"] = dados_2024["SITUAÇÃO ATUAL"].apply(lambda x: 1 if x != "MATRICULADO" else 0)

# Contar evasão por categoria de número de escolas no município
evasao_por_qtd_escolas = dados_2024.groupby("CATEGORIA_QT_ESCOLAS")["EVASAO"].agg(["count", "sum"]).reset_index()
evasao_por_qtd_escolas.columns = ["CATEGORIA_QT_ESCOLAS", "TOTAL_PARTICIPANTES", "TOTAL_EVADIDOS"]
evasao_por_qtd_escolas["TAXA_EVASAO"] = (evasao_por_qtd_escolas["TOTAL_EVADIDOS"] / evasao_por_qtd_escolas["TOTAL_PARTICIPANTES"]) * 100

# Adicionar a contagem de municípios por categoria
contagem_municipios = dados_2024.groupby("CATEGORIA_QT_ESCOLAS", observed=False)["ID_MUNICIPIO"].nunique().reset_index()
contagem_municipios.columns = ["CATEGORIA_QT_ESCOLAS", "QT_MUNICIPIOS"]

# Incorporar a contagem ao DataFrame principal
evasao_por_qtd_escolas = evasao_por_qtd_escolas.merge(contagem_municipios, on="CATEGORIA_QT_ESCOLAS", how="left")

# Salvar os resultados corretamente
evasao_por_qtd_escolas.to_csv("evasao_por_qtd_escolas.csv", index=False)

#=========================#
#       STREAMLIT         #
#=========================#

# Título do App
st.title("Taxa de Evasão no PRODITEC por Número de Escolas no Município")
st.write("Este gráfico mostra a relação entre a taxa de evasão e o número total de escolas nos municípios.")

# Corrigir a formatação dos intervalos no eixo X
evasao_por_qtd_escolas["CATEGORIA_QT_ESCOLAS"] = (
    evasao_por_qtd_escolas["CATEGORIA_QT_ESCOLAS"]
    .astype(str)
    .str.replace("[\(\)\[\]]", "", regex=True)  # Remove colchetes e parênteses corretamente
    .str.replace(", ", " - ")  # Ajusta o formato para "x - y"
)

# Ajustar a formatação para exibir apenas 2 casas decimais na taxa de evasão
evasao_por_qtd_escolas["TAXA_EVASAO"] = evasao_por_qtd_escolas["TAXA_EVASAO"].round(2)

# Criar gráfico interativo com Plotly
fig = px.bar(
    evasao_por_qtd_escolas,
    x="CATEGORIA_QT_ESCOLAS",
    y="TAXA_EVASAO",
    labels={
        "CATEGORIA_QT_ESCOLAS": "Número de Escolas no Município (Faixas)",
        "TAXA_EVASAO": "Taxa de Evasão (%)"
    },
    title="Taxa de Evasão por Número de Escolas no Município",
    color="TAXA_EVASAO",
    color_continuous_scale="reds",
    hover_data={"QT_MUNICIPIOS": True, "TAXA_EVASAO": ":.2f"}  # Mostrar somente 2 casas decimais no hover
)

# Ordenar os intervalos corretamente no eixo X
fig.update_layout(
    xaxis=dict(
        title="Número de Escolas no Município (Faixas)",
        tickangle=-45,
        categoryorder="array",
        categoryarray=sorted(
            evasao_por_qtd_escolas["CATEGORIA_QT_ESCOLAS"],
            key=lambda x: float(x.split(" - ")[0])  # Ordena pelo número inicial do intervalo
        )
    ),
    yaxis=dict(title="Taxa de Evasão (%)"),
    coloraxis_colorbar=dict(title="Taxa de Evasão (%)"),
    showlegend=False
)

# Ajustar a exibição do hover para incluir informações detalhadas
fig.update_traces(
    hovertemplate="<b>Faixa de Escolas:</b> %{x}<br>" +
                  "<b>Taxa de Evasão:</b> %{y:.2f}%<br>" +
                  "<b>Quantidade de Municípios:</b> %{customdata[0]}<br>"
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

# Exibir a tabela com os dados usados no gráfico (opcional)
st.write("### Dados Utilizados no Gráfico")
st.dataframe(evasao_por_qtd_escolas)
