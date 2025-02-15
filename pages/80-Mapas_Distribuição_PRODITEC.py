import streamlit as st
import streamlit.components.v1 as components
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


# Função para exibir um arquivo HTML corretamente
def exibir_html(arquivo_html, titulo):
    """Lê um arquivo HTML e exibe seu conteúdo no Streamlit corretamente."""
    try:
        with open(arquivo_html, "r", encoding="utf-8") as f:
            html_content = f.read()

        st.subheader(titulo)  # Adiciona um título para cada mapa
        components.html(html_content, height=600, scrolling=True)  # Renderiza o HTML corretamente

    except FileNotFoundError:
        st.error(f"❌ Arquivo não encontrado: {arquivo_html}")


# 🔹 Exibir os mapas corretamente
exibir_html("mapa_2024_bolha_distribuição.html", "📍 Distribuição dos Cursistas - 2024/2")
exibir_html("mapa_2025_bolha_distribuição.html", "📍 Distribuição dos Cursistas - 2025/1")
exibir_html("mapa_total_bolha_distribuição.html", "📍 Distribuição dos Cursistas - Total")
