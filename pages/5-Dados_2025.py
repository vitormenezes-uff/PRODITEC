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


# Função para carregar os dados a partir de um arquivo CSV local
@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"Erro ao carregar dados do arquivo: {file_path}")
        return pd.DataFrame()


# Caminho do arquivo de dados 2025
data_2025_path = "dados_2025.csv"
df_2025 = load_data(data_2025_path)

if df_2025.empty:
    st.error("Dados de 2025 não disponíveis.")
else:
    # Garantir que a coluna "SIGLA UF" esteja em maiúsculo
    if "SIGLA UF" in df_2025.columns:
        df_2025["SIGLA UF"] = df_2025["SIGLA UF"].str.upper()

    # Mapeamento das UFs para suas respectivas regiões (incluindo DF em CENTRO-OESTE)
    regioes_map = {
        'AC': 'NORTE', 'AP': 'NORTE', 'AM': 'NORTE', 'PA': 'NORTE',
        'RO': 'NORTE', 'RR': 'NORTE', 'TO': 'NORTE',
        'AL': 'NORDESTE', 'BA': 'NORDESTE', 'CE': 'NORDESTE', 'MA': 'NORDESTE',
        'PB': 'NORDESTE', 'PE': 'NORDESTE', 'PI': 'NORDESTE', 'RN': 'NORDESTE',
        'SE': 'NORDESTE',
        'DF': 'CENTRO-OESTE', 'GO': 'CENTRO-OESTE', 'MT': 'CENTRO-OESTE', 'MS': 'CENTRO-OESTE',
        'ES': 'SUDESTE', 'MG': 'SUDESTE', 'RJ': 'SUDESTE', 'SP': 'SUDESTE',
        'PR': 'SUL', 'RS': 'SUL', 'SC': 'SUL'
    }
    if "SIGLA UF" in df_2025.columns:
        df_2025["REGIAO"] = df_2025["SIGLA UF"].map(regioes_map)

    # Dicionário que mapeia as siglas para os nomes completos das UFs
    uf_names = {
        'AC': 'Acre',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'PA': 'Pará',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'TO': 'Tocantins',
        'AL': 'Alagoas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'MA': 'Maranhão',
        'PB': 'Paraíba',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RN': 'Rio Grande do Norte',
        'SE': 'Sergipe',
        'DF': 'Distrito Federal',
        'GO': 'Goiás',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'ES': 'Espírito Santo',
        'MG': 'Minas Gerais',
        'RJ': 'Rio de Janeiro',
        'SP': 'São Paulo',
        'PR': 'Paraná',
        'RS': 'Rio Grande do Sul',
        'SC': 'Santa Catarina'
    }

    # Criação das abas principais
    tabs = st.tabs(["Visão Geral", "Regiões", "Estatísticas por Estado", "Estatísticas por Região"])

    ##########################
    # Aba 1: Visão Geral
    with tabs[0]:
        st.subheader("Visualização Completa dos Dados de 2025")
        st.dataframe(df_2025)

        st.subheader("Distribuição por UF")
        if "SIGLA UF" in df_2025.columns:
            uf_counts = df_2025["SIGLA UF"].value_counts().reset_index()
            uf_counts.columns = ["SIGLA UF", "Quantidade"]
            fig_bar = px.bar(
                uf_counts,
                x="SIGLA UF",
                y="Quantidade",
                labels={"SIGLA UF": "UF", "Quantidade": "Número de Alunos"}
            )
            st.plotly_chart(fig_bar, use_container_width=True, key="fig_bar_2025")

        st.subheader("Distribuição por Região")
        if "REGIAO" in df_2025.columns:
            reg_counts = df_2025["REGIAO"].value_counts().reset_index()
            reg_counts.columns = ["REGIAO", "Quantidade"]
            fig_pie = px.pie(
                reg_counts,
                names="REGIAO",
                values="Quantidade"
            )
            st.plotly_chart(fig_pie, use_container_width=True, key="fig_pie_2025")

        st.subheader("Taxa de Evasão (2025-2) - Percentual por SITUAÇÃO ATUAL (por Estado)")
        if "SIGLA UF" in df_2025.columns and "SITUAÇÃO ATUAL" in df_2025.columns:
            df_group_situacao = df_2025.groupby(["SIGLA UF", "SITUAÇÃO ATUAL"]).size().reset_index(name="count")
            df_group_situacao["total"] = df_group_situacao.groupby("SIGLA UF")["count"].transform("sum")
            df_group_situacao["percentage"] = (df_group_situacao["count"] / df_group_situacao["total"]) * 100
            fig_situacao = px.bar(
                df_group_situacao,
                x="SIGLA UF",
                y="percentage",
                color="SITUAÇÃO ATUAL",
                text="percentage",
                barmode="stack"
            )
            fig_situacao.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            st.plotly_chart(fig_situacao, use_container_width=True, key="fig_situacao_inicio")
        else:
            st.write("Dados de SITUAÇÃO ATUAL não disponíveis.")

        st.subheader("Taxa de Evasão (2025-2) - Números Absolutos por SITUAÇÃO ATUAL (por Estado)")
        if "SIGLA UF" in df_2025.columns and "SITUAÇÃO ATUAL" in df_2025.columns:
            df_group_situacao_abs = df_2025.groupby(["SIGLA UF", "SITUAÇÃO ATUAL"]).size().reset_index(name="count")
            fig_situacao_abs = px.bar(
                df_group_situacao_abs,
                x="SIGLA UF",
                y="count",
                color="SITUAÇÃO ATUAL",
                text="count",
                barmode="stack"
            )
            fig_situacao_abs.update_traces(texttemplate='%{text}', textposition='inside')
            st.plotly_chart(fig_situacao_abs, use_container_width=True, key="fig_situacao_abs")
        else:
            st.write("Dados de SITUAÇÃO ATUAL não disponíveis.")

    ##########################
    # Aba 2: Regiões
    with tabs[1]:
        st.subheader("Gráficos de Pizza por Região")
        if "REGIAO" in df_2025.columns:
            reg_counts = df_2025["REGIAO"].value_counts().reset_index()
            reg_counts.columns = ["REGIAO", "Quantidade"]
            fig_global = px.pie(
                reg_counts,
                names="REGIAO",
                values="Quantidade"
            )
            st.plotly_chart(fig_global, use_container_width=True, key="fig_global_2025")

        ordered_regioes = ["NORTE", "NORDESTE", "CENTRO-OESTE", "SUDESTE", "SUL"]
        region_tabs = st.tabs(ordered_regioes)
        for i, regiao in enumerate(ordered_regioes):
            with region_tabs[i]:
                st.subheader(f"Região: {regiao}")
                df_regiao = df_2025[df_2025["REGIAO"] == regiao]
                if not df_regiao.empty and "SIGLA UF" in df_regiao.columns:
                    uf_counts = df_regiao["SIGLA UF"].value_counts().reset_index()
                    uf_counts.columns = ["SIGLA UF", "Quantidade"]
                    labels_full = uf_counts["SIGLA UF"].map(uf_names)
                    fig_region = px.pie(
                        uf_counts,
                        names=labels_full,
                        values="Quantidade"
                    )
                    fig_region.update_traces(hovertemplate='<b>%{label}</b><br>Quantidade: %{value}<extra></extra>')
                    st.plotly_chart(fig_region, use_container_width=True, key=f"fig_region_{regiao}")
                else:
                    st.write(f"Dados não disponíveis para a região {regiao}.")

    ##########################
    # Aba 3: Estatísticas por Estado
    with tabs[2]:
        st.subheader("Percentual por DEPENDÊNCIA ADMINISTRATIVA (por Estado)")
        if "SIGLA UF" in df_2025.columns:
            if "DEPENDÊNCIA ADMINISTRATIVA" in df_2025.columns:
                col_dep = "DEPENDÊNCIA ADMINISTRATIVA"
            elif "DEPENDENCIA ADMINISTRATIVA" in df_2025.columns:
                col_dep = "DEPENDENCIA ADMINISTRATIVA"
            else:
                col_dep = None
                st.error("Coluna de dependência administrativa não encontrada.")
            if col_dep:
                df_group_dep = df_2025.groupby(["SIGLA UF", col_dep]).size().reset_index(name="count")
                df_group_dep["total"] = df_group_dep.groupby("SIGLA UF")["count"].transform("sum")
                df_group_dep["percentage"] = (df_group_dep["count"] / df_group_dep["total"]) * 100
                fig_dep = px.bar(
                    df_group_dep,
                    x="SIGLA UF",
                    y="percentage",
                    color=col_dep,
                    text="percentage",
                    barmode="stack"
                )
                fig_dep.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
                st.plotly_chart(fig_dep, use_container_width=True, key="fig_dep")

        st.subheader("Percentual por CARGO OU FUNÇÃO DO CURSISTA (por Estado)")
        if "SIGLA UF" in df_2025.columns and "CARGO OU FUNÇÃO DO CURSISTA" in df_2025.columns:
            df_group_cargo = df_2025.groupby(["SIGLA UF", "CARGO OU FUNÇÃO DO CURSISTA"]).size().reset_index(
                name="count")
            df_group_cargo["total"] = df_group_cargo.groupby("SIGLA UF")["count"].transform("sum")
            df_group_cargo["percentage"] = (df_group_cargo["count"] / df_group_cargo["total"]) * 100
            fig_cargo = px.bar(
                df_group_cargo,
                x="SIGLA UF",
                y="percentage",
                color="CARGO OU FUNÇÃO DO CURSISTA",
                text="percentage",
                barmode="stack"
            )
            fig_cargo.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            st.plotly_chart(fig_cargo, use_container_width=True, key="fig_cargo")
        else:
            st.write("Dados de CARGO OU FUNÇÃO DO CURSISTA não disponíveis.")

        st.subheader("Percentual por FORMAÇÃO (por Estado)")
        if "SIGLA UF" in df_2025.columns and "FORMAÇÃO" in df_2025.columns:
            df_group_formacao = df_2025.groupby(["SIGLA UF", "FORMAÇÃO"]).size().reset_index(name="count")
            df_group_formacao["total"] = df_group_formacao.groupby("SIGLA UF")["count"].transform("sum")
            df_group_formacao["percentage"] = (df_group_formacao["count"] / df_group_formacao["total"]) * 100
            fig_formacao = px.bar(
                df_group_formacao,
                x="SIGLA UF",
                y="percentage",
                color="FORMAÇÃO",
                text="percentage",
                barmode="stack"
            )
            fig_formacao.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            st.plotly_chart(fig_formacao, use_container_width=True, key="fig_formacao")
        else:
            st.write("Dados de FORMAÇÃO não disponíveis.")

        st.subheader("Taxa de Evasão (2025-2) - Percentual por SITUAÇÃO ATUAL (por Estado)")
        if "SIGLA UF" in df_2025.columns and "SITUAÇÃO ATUAL" in df_2025.columns:
            df_group_situacao = df_2025.groupby(["SIGLA UF", "SITUAÇÃO ATUAL"]).size().reset_index(name="count")
            df_group_situacao["total"] = df_group_situacao.groupby("SIGLA UF")["count"].transform("sum")
            df_group_situacao["percentage"] = (df_group_situacao["count"] / df_group_situacao["total"]) * 100
            fig_situacao = px.bar(
                df_group_situacao,
                x="SIGLA UF",
                y="percentage",
                color="SITUAÇÃO ATUAL",
                text="percentage",
                barmode="stack"
            )
            fig_situacao.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            st.plotly_chart(fig_situacao, use_container_width=True, key="fig_situacao")
        else:
            st.write("Dados de SITUAÇÃO ATUAL não disponíveis.")

    ##########################
    # Aba 4: Estatísticas por Região
    with tabs[3]:
        st.subheader("Percentual por DEPENDÊNCIA ADMINISTRATIVA (por Região)")
        if "REGIAO" in df_2025.columns:
            if "DEPENDÊNCIA ADMINISTRATIVA" in df_2025.columns:
                col_dep = "DEPENDÊNCIA ADMINISTRATIVA"
            elif "DEPENDENCIA ADMINISTRATIVA" in df_2025.columns:
                col_dep = "DEPENDENCIA ADMINISTRATIVA"
            else:
                col_dep = None
                st.error("Coluna de dependência administrativa não encontrada.")
            if col_dep:
                df_group_dep_reg = df_2025.groupby(["REGIAO", col_dep]).size().reset_index(name="count")
                df_group_dep_reg["total"] = df_group_dep_reg.groupby("REGIAO")["count"].transform("sum")
                df_group_dep_reg["percentage"] = (df_group_dep_reg["count"] / df_group_dep_reg["total"]) * 100
                fig_dep_reg = px.bar(
                    df_group_dep_reg,
                    x="REGIAO",
                    y="percentage",
                    color=col_dep,
                    text="percentage",
                    barmode="stack"
                )
                fig_dep_reg.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
                st.plotly_chart(fig_dep_reg, use_container_width=True, key="fig_dep_reg")

        st.subheader("Percentual por CARGO OU FUNÇÃO DO CURSISTA (por Região)")
        if "REGIAO" in df_2025.columns and "CARGO OU FUNÇÃO DO CURSISTA" in df_2025.columns:
            df_group_cargo_reg = df_2025.groupby(["REGIAO", "CARGO OU FUNÇÃO DO CURSISTA"]).size().reset_index(
                name="count")
            df_group_cargo_reg["total"] = df_group_cargo_reg.groupby("REGIAO")["count"].transform("sum")
            df_group_cargo_reg["percentage"] = (df_group_cargo_reg["count"] / df_group_cargo_reg["total"]) * 100
            fig_cargo_reg = px.bar(
                df_group_cargo_reg,
                x="REGIAO",
                y="percentage",
                color="CARGO OU FUNÇÃO DO CURSISTA",
                text="percentage",
                barmode="stack"
            )
            fig_cargo_reg.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            st.plotly_chart(fig_cargo_reg, use_container_width=True, key="fig_cargo_reg")
        else:
            st.write("Dados de CARGO OU FUNÇÃO DO CURSISTA não disponíveis.")

        st.subheader("Percentual por FORMAÇÃO (por Região)")
        if "REGIAO" in df_2025.columns and "FORMAÇÃO" in df_2025.columns:
            df_group_formacao_reg = df_2025.groupby(["REGIAO", "FORMAÇÃO"]).size().reset_index(name="count")
            df_group_formacao_reg["total"] = df_group_formacao_reg.groupby("REGIAO")["count"].transform("sum")
            df_group_formacao_reg["percentage"] = (df_group_formacao_reg["count"] / df_group_formacao_reg[
                "total"]) * 100
            fig_formacao_reg = px.bar(
                df_group_formacao_reg,
                x="REGIAO",
                y="percentage",
                color="FORMAÇÃO",
                text="percentage",
                barmode="stack"
            )
            fig_formacao_reg.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            st.plotly_chart(fig_formacao_reg, use_container_width=True, key="fig_formacao_reg")
        else:
            st.write("Dados de FORMAÇÃO não disponíveis.")

        st.subheader("Taxa de Evasão (por SITUAÇÃO ATUAL, por Região)")
        if "REGIAO" in df_2025.columns and "SITUAÇÃO ATUAL" in df_2025.columns:
            df_group_situacao_reg = df_2025.groupby(["REGIAO", "SITUAÇÃO ATUAL"]).size().reset_index(name="count")
            df_group_situacao_reg["total"] = df_group_situacao_reg.groupby("REGIAO")["count"].transform("sum")
            df_group_situacao_reg["percentage"] = (df_group_situacao_reg["count"] / df_group_situacao_reg[
                "total"]) * 100
            fig_situacao_reg = px.bar(
                df_group_situacao_reg,
                x="REGIAO",
                y="percentage",
                color="SITUAÇÃO ATUAL",
                text="percentage",
                barmode="stack"
            )
            fig_situacao_reg.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            st.plotly_chart(fig_situacao_reg, use_container_width=True, key="fig_situacao_reg")
        else:
            st.write("Dados de SITUAÇÃO ATUAL não disponíveis.")
