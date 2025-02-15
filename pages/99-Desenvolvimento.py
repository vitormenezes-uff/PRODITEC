import streamlit as st
from config_pagina import configurar_pagina
from carregador_texto import carregar_texto

# Nome do arquivo Markdown correspondente
nome_arquivo_md = "Desenvolvimento.md"

# Configurar a página com base no nome do script
configurar_pagina("99-Desenvolvimento.py")

# Exibir o conteúdo do arquivo Markdown
# st.markdown(carregar_texto(nome_arquivo_md))
