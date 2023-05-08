# praktikum_new_diplom
Запуск проекта через Docker для разработки:
docker-compose up

Может подняться не сразу, со второй попытки заработал у меня. 

Документация к api открывается по адресу: http://localhost/api/docs/


Установить зависимости:
pip install -r requirements.txt 

Создать файл зависимостей:
pip freeze > requirements.txt

создать проект django:
django-admin startproject projectname
создать супер пользователя:
python manage.py createsuperuser

POSTGRES_PASSWORD MyPassword123

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 


Создать ВМ:
прописать имя ВМ
выбрать Ubuntu 20.04
прописать Логин
прописать SSH-ключ  для его получения 
в командной строке ввести:(cat ~/.ssh/id_rsa.pub)

Подключение к ВМ:
в терминале ввести:  ssh admin@158.160.2.202
admin - это логин который прописали при создании ВМ
IP - тот что выдали когда ВМ создалась (Публичный IPv4)

Ввести команды:
sudo apt update
sudo apt upgrade -y

Спринт 14/18 → Тема 2/3: Запуск проекта на сервере → Урок 7/13
Устрановка nginx:
sudo apt install nginx -y 
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
Проверить сработало ли:
sudo ufw status
Если Status: inactive то повторить: sudo ufw enable

Запуск nginx:
sudo systemctl start nginx (не запускай пока)


Спринт 16 финальный проект Подготовьте сервер
sudo systemctl stop nginx - остановить nginx если запущен


Установить Докер
sudo apt install docker.io 

Установите docker-compose
Проверить версию можно тут:
https://github.com/docker/compose/releases
Установить docker-compose:
sudo curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

Затем необходимо задать правильные разрешения, чтобы сделать команду docker-compose исполняемой:
sudo chmod +x /usr/local/bin/docker-compose

Чтобы проверить успешность установки, запустите следующую команду:
docker-compose --version

Скопируйте файлы docker-compose.yaml и nginx/default.conf
из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml 
и home/<ваш_username>/nginx.conf соответственно.

scp docker-compose.yml admin@158.160.2.202:/home/admin/docker-compose.yml
scp nginx.conf admin@158.160.2.202:/home/admin/nginx.conf


scp -r frontend admin@158.160.12.203:/home/admin/frontend  - не надо вроде




docker backend

FROM python:3.7-slim

WORKDIR /app

COPY ./ .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]


work flow

# .github/workflows/**main.yml**
name: Django-app workflow

on: [push]

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.7

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip 
          pip install flake8 pep8-naming flake8-broken-line flake8-return flake8-isort
          pip install -r backend/requirements.txt 

      - name: Test with flake8 and django tests
        run: |
          python -m flake8

  build_and_push_to_docker_hub:
    name: Push Docker image to Docker Hub
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repo
        uses: actions/checkout@v2
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      - name: Login to Docker
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Push backend to Docker Hub
        uses: docker/build-push-action@v2
        with:
          push: true
          context: backend/
          no-cache: true
          tags: ${{ secrets.DOCKER_USERNAME }}/foodgram-project
      - name: Push frontend to Docker Hub
        uses: docker/build-push-action@v2
        with:
          push: true
          context: frontend/
          no-cache: true
          tags: ${{ secrets.DOCKER_USERNAME }}/foodgram-project-frontend

  deploy:
    runs-on: ubuntu-latest
    needs: build_and_push_to_docker_hub
    steps:
      - name: executing remote ssh commands to deploy
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            sudo docker pull ${{ secrets.DOCKER_USERNAME }}/foodgram-project
            sudo docker pull ${{ secrets.DOCKER_USERNAME }}/foodgram-project-frontend
            sudo docker-compose stop
            sudo docker-compose rm backend frontend
            rm .env
            touch .env
            echo DB_ENGINE=${{ secrets.DB_ENGINE }} >> .env
            echo DB_NAME=${{ secrets.DB_NAME }} >> .env
            echo POSTGRES_USER=${{ secrets.POSTGRES_USER }} >> .env
            echo POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }} >> .env
            echo DB_HOST=${{ secrets.DB_HOST }} >> .env
            echo DB_PORT=${{ secrets.DB_PORT }} >> .env
            sudo docker-compose up -d