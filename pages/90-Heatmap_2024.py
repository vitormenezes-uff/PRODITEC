import streamlit as st
import os
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

# Caminho para o arquivo HTML
html_file = "mapa_brasil_2024_2.html"

if os.path.exists(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    # Exibe o conteúdo HTML no Streamlit
    st.components.v1.html(html_content, height=600, scrolling=True)
else:
    st.error("Arquivo 'mapa_brasil_2024_2.html' não encontrado.")
