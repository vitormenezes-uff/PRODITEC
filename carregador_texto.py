import os
import streamlit as st

def carregar_texto(nome_arquivo):
    """Carrega um arquivo Markdown da pasta 'descricoes' e retorna seu conteúdo."""
    caminho_arquivo = os.path.join("descricoes", nome_arquivo)
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return f.read()
    return f"⚠️ **Aviso:** Arquivo de descrição `{nome_arquivo}` não encontrado."
