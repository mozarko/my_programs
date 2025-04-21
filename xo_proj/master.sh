#!/bin/bash

# Переменные
DOCKERFILE_PATH="/home/mike/Documents/mozarko_github/my_programs/xo_proj/"
IMAGE_NAME="cr.yandex/crpj07mj889kvh8ss9gs/xo:latest"
REMOTE_SERVER="myvps"  # Замените на IP и пользователя вашего сервера

# Сборка Docker-образа
echo "Сборка Docker-образа..."
docker build -t $IMAGE_NAME $DOCKERFILE_PATH

# Проверка успешности сборки
if [ $? -ne 0 ]; then
  echo "Ошибка сборки образа."
  exit 1
fi

# Пуш в Yandex Cloud Container Registry
echo "Пуш Docker-образа в Yandex Cloud..."
docker push $IMAGE_NAME

# Проверка успешности пуша
if [ $? -ne 0 ]; then
  echo "Ошибка при пуше в реестр."
  exit 1
fi

echo "Docker-образ успешно собран и загружен в реестр!"

# Перезапуск контейнеров на сервере
echo "Перезапуск контейнеров на сервере..."
ssh $REMOTE_SERVER << EOF
export DOCKER_CREDENTIAL_HELPER=/root/yandex-cloud/bin/docker-credential-yc
export PATH=\$PATH:/root/yandex-cloud/bin
  # Останавливаем и удаляем текущие контейнеры
  docker-compose -f /root/xo_proj/docker-compose.server.yml down
  
  # Тянем обновленный образ из реестра
  docker-compose -f /root/xo_proj/docker-compose.server.yml pull
  
  # Запускаем контейнеры с новым образом в фоновом режиме
  docker-compose -f /root/xo_proj/docker-compose.server.yml up -d
  docker image prune -f
EOF

# Проверка успешности перезапуска
if [ $? -ne 0 ]; then
  echo "Ошибка при перезапуске контейнеров на сервере."
  exit 1
fi

echo "Контейнеры успешно перезапущены на сервере!"

