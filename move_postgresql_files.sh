#!/bin/bash

# Define os caminhos de origem e destino
SOURCE_DIR="/c/Users/eder-/Desktop/Iphone/a121_backend/a121_backend"
DEST_DIR="/c/Program\ Files/PostgreSQL/17/bin"

# Lista de arquivos a mover
FILES=(
    "edb_npgsql.exe"
    "edb_pgagent_pg17.exe"
    "edb_pgbouncer.exe"
    "edb_pgjdbc.exe"
    "edb_psqlodbc.exe"
    "postgis_3_5_pg17.exe"
)

# Verifica se o diretório de destino existe
if [ ! -d "$DEST_DIR" ]; then
    echo "Erro: O diretório de destino $DEST_DIR não existe. Verifique se o PostgreSQL está instalado corretamente."
    exit 1
fi

# Move cada arquivo
for FILE in "${FILES[@]}"; do
    if [ -f "$SOURCE_DIR/$FILE" ]; then
        echo "Movendo $FILE para $DEST_DIR..."
        mv "$SOURCE_DIR/$FILE" "$DEST_DIR/$FILE"
    else
        echo "Arquivo $FILE não encontrado em $SOURCE_DIR. Pulando..."
    fi
done

# Adiciona os arquivos ao .gitignore para evitar que sejam rastreados pelo Git
echo "Adicionando arquivos ao .gitignore..."
for FILE in "${FILES[@]}"; do
    echo "a121_backend/$FILE" >> .gitignore
done

# Verifica se o .gitignore já está no Git, se não, adiciona
if [ -f ".gitignore" ]; then
    git add .gitignore
    git commit -m "Atualizando .gitignore para ignorar arquivos do PostgreSQL"
fi
