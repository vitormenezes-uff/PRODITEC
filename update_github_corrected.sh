#!/bin/bash

# Nome do repositório
REPO_URL="https://github.com/Vitorbiouerj/DadosPRODITEC.git"

# Definir arquivos que devem ser ignorados se forem muito grandes
LARGE_FILES=$(find . -type f -size +100M)

if [ -n "$LARGE_FILES" ]; then
    echo "Os seguintes arquivos excedem 100MB e não serão commitados:"
    echo "$LARGE_FILES"
    git rm --cached $LARGE_FILES 2>/dev/null
fi

# Adiciona os arquivos ao commit, ignorando arquivos muito grandes
git add .

# Solicita a mensagem do commit
echo "Digite a mensagem do commit:"
read COMMIT_MSG

# Cria o commit
git commit -m "$COMMIT_MSG"

# Verifica se o repositório remoto está atualizado
git pull --rebase $REPO_URL main

# Faz o push das alterações
git push $REPO_URL main

echo "Repositório atualizado com sucesso."
