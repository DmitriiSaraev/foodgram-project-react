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
и home/<ваш_username>/nginx/default.conf соответственно.

scp docker-compose.yml admin@158.160.2.202:/home/admin/docker-compose.yml
scp nginx.conf admin@158.160.2.202:/home/admin/nginx/nginx.conf


scp -r frontend admin@158.160.12.203:/home/admin/frontend  - не надо вроде

