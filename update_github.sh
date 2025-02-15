#!/bin/bash

echo "Carregando credenciais do GitHub..."
git config --global credential.helper store

echo "Atualizando Git hooks..."
git config --global init.defaultBranch main
git init
git lfs install

echo "Verificando alterações locais..."
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "Alterações locais detectadas. Guardando no stash..."
    git stash push -m "Backup antes do pull"
fi

echo "Sincronizando repositório local com remoto..."
git pull --rebase origin main

if git stash list | grep -q "Backup antes do pull"; then
    echo "Reaplicando alterações locais..."
    git stash pop
fi

# Gera a mensagem do commit no formato ANO-MÊS-DIA HORA:MINUTO
commit_message="atualização automática número $(date '+%Y-%m-%d %H:%M')"

echo "Criando commit com a mensagem: '$commit_message'"
git add .
git commit -m "$commit_message"

echo "Fazendo push dos arquivos para o GitHub com Git LFS..."
git push origin main

echo "Sincronização concluída com sucesso!"

