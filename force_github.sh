#!/bin/bash

# Nome do repositório remoto
REPO_URL="https://github.com/Vitorbiouerj/DadosPRODITEC.git"
BRANCH="main"

echo "ATENÇÃO: Este script removerá completamente o histórico do Git e recriará o repositório do zero."
read -p "Tem certeza que deseja continuar? (sim/não): " CONFIRM

if [ "$CONFIRM" != "sim" ]; then
    echo "Operação cancelada."
    exit 1
fi

# Remover o repositório Git local
echo "Removendo histórico do Git..."
rm -rf .git

# Recriar o repositório Git
echo "Recriando o repositório Git..."
git init
git remote add origin $REPO_URL
git checkout -b $BRANCH

# Buscar arquivos maiores que 100MB e adicioná-los ao .gitignore
LARGE_FILES=$(find . -type f -size +100M)

if [ -n "$LARGE_FILES" ]; then
    echo "Os seguintes arquivos excedem 100MB e serão adicionados ao .gitignore:"
    echo "$LARGE_FILES"

    # Adicionar arquivos grandes ao .gitignore
    echo "$LARGE_FILES" >> .gitignore
    sort -u -o .gitignore .gitignore  # Remover duplicatas do .gitignore
fi

# Adicionar todos os arquivos ao novo repositório
git add --all

# Solicitar a mensagem do commit
echo "Digite a mensagem do commit:"
read COMMIT_MSG

# Criar o primeiro commit no novo histórico
git commit -m "$COMMIT_MSG"

# Forçar o envio do novo histórico para o GitHub
echo "Forçando o upload de todos os arquivos para o repositório GitHub..."
git push --force origin $BRANCH

echo "Repositório resetado e sincronizado com sucesso."

