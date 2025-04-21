#!/bin/bash

# Конфигурация
USER="root"
HOST="myvps"
REMOTE_DIR="/root/xo_proj"

# Абсолютный путь к проекту
LOCAL_PROJECT_DIR="/home/mike/Documents/mozarko_github/my_programs/xo_proj/"

# Локальные файлы/папки для копирования
FILES=(
  "$LOCAL_PROJECT_DIR/docker-compose.server.yml"
)

echo "📦 Копирую файлы на сервер $HOST..."

# Копирование
scp -r "${FILES[@]}" $USER@$HOST:$REMOTE_DIR

echo "✅ Файлы скопированы."

