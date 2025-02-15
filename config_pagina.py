import streamlit as st
import os
import unicodedata
import re
from carregador_texto import carregar_texto

def remover_acentos(texto):
    """
    Remove acentos e caracteres especiais do nome do arquivo para evitar problemas de compatibilidade.
    """
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def remover_prefixo_numerico(texto):
    """
    Remove números seguidos de um traço no início do texto (exemplo: '1-Dados_IBGE_2023' -> 'Dados_IBGE_2023').
    """
    return re.sub(r'^\d+-', '', texto)  # Remove qualquer número no início seguido de "-"

def configurar_pagina(nome_arquivo):
    """
    Configura a página do Streamlit com base no nome do arquivo Python que a chama.

    - Define o título da página e da interface com base no nome do arquivo.
    - Busca automaticamente o arquivo correspondente na pasta 'descricoes'.
    - Garante que o caminho do arquivo seja correto no ambiente de deploy.
    """
    # Obtém o caminho absoluto da pasta descricoes
    pasta_descricoes = os.path.abspath("descricoes")

    # Verifica se a pasta existe
    if not os.path.exists(pasta_descricoes):
        st.error(f"⚠️ Erro: A pasta '{pasta_descricoes}' não foi encontrada.")
        print(f"⚠️ Erro: A pasta '{pasta_descricoes}' não foi encontrada.")
        return

    # Lista todos os arquivos .md disponíveis
    arquivos_md = [arquivo for arquivo in os.listdir(pasta_descricoes) if arquivo.endswith(".md")]
    print(f"Arquivos disponíveis na pasta '{pasta_descricoes}': {arquivos_md}")  # Depuração

    # Garante que o nome do arquivo está formatado corretamente e remove acentos
    titulo_pagina = nome_arquivo.replace(".py", "")  # Nome base do arquivo
    titulo_exibicao = remover_prefixo_numerico(titulo_pagina).replace("_", " ")  # Remove números e melhora exibição
    titulo_sem_acentos = remover_acentos(titulo_pagina)

    st.set_page_config(page_title=titulo_exibicao, layout="wide")
    st.title(titulo_exibicao)

    # Procurar o arquivo correto, comparando sem acentos
    arquivo_correspondente = None
    for arquivo in arquivos_md:
        nome_arquivo_md = arquivo.replace(".md", "")
        nome_arquivo_md_sem_acentos = remover_acentos(nome_arquivo_md)

        if titulo_sem_acentos.lower() == nome_arquivo_md_sem_acentos.lower():
            arquivo_correspondente = os.path.join(pasta_descricoes, arquivo)
            break

    # Depuração: Verificar se o nome do arquivo foi encontrado corretamente
    print(f"Tentando carregar o arquivo: {arquivo_correspondente}")

    # Verificar se o arquivo foi encontrado e carregar
    if arquivo_correspondente and os.path.exists(arquivo_correspondente):
        st.markdown(carregar_texto(arquivo_correspondente))
    else:
        st.error(f"⚠️ Erro: Nenhum arquivo correspondente encontrado para '{titulo_pagina}.md'.")
        print(f"⚠️ Erro: Nenhum arquivo correspondente encontrado para '{titulo_pagina}.md'.")

    # Configuração da barra lateral
    st.sidebar.title("Menu")
    st.sidebar.markdown("""
    - Use os itens da barra lateral para navegar entre dados de 2024/2 e 2025/1
    - Use as abas para navegar nos diferentes tipos de visualizações
    - Caso queira usar um tema claro, clique nos 3 pontos, vá em Settings e mude o "Choose app theme, colors and fonts" para Light
    - **Caso esteja visualizando no celular, clique nos 3 pontos, vá em Settings e desmarque o "Wide Mode"**
    
    ---
    
    Desenvolvido por Vitor Lima Menezes
    """)
