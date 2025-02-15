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


# Verificar se o arquivo do mapa existe
mapa_path = "meu_mapa.html"

if not os.path.exists(mapa_path):
    st.error("O arquivo 'meu_mapa.html' não foi encontrado. Execute o script de geração do mapa antes de visualizar.")
else:
    st.title("Mapa Interativo de Escolas no Brasil")
    st.write("Este mapa apresenta a distribuição das escolas no Brasil, com diferenciação por estados e municípios.")

    # Carregar o mapa HTML
    with open(mapa_path, "r", encoding="utf-8") as f:
        mapa_html = f.read()

    # Exibir o mapa no Streamlit
    st.components.v1.html(mapa_html, height=600, scrolling=True)
