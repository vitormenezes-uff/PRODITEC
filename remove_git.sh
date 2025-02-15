#!/bin/bash

echo "🚀 Iniciando remoção completa do repositório Git..."

# Verifica se estamos dentro de um repositório Git
if [ ! -d ".git" ]; then
    echo "❌ Nenhum repositório Git encontrado neste diretório!"
    exit 1
fi

# Remove a pasta .git (apaga o histórico do repositório)
echo "🗑️ Removendo pasta .git/..."
rm -rf .git

# Remove arquivos e configurações do Git LFS, se existirem
if [ -d ".git/lfs" ]; then
    echo "🗑️ Removendo pasta .git/lfs/..."
    rm -rf .git/lfs
fi

# Remove o .gitattributes e .gitignore, se existirem
if [ -f ".gitattributes" ]; then
    echo "🗑️ Removendo .gitattributes..."
    rm -f .gitattributes
fi

# Finalização
echo "✅ Repositório Git removido com sucesso!"
echo "📂 Seus arquivos continuam intactos. Agora você pode criar um novo repositório e fazer o upload novamente."

exit 0

