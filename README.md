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


scp -r frontend admin@158.160.12.203:/home/admin/frontend
scp nginx.conf admin@158.160.12.203:/home/admin/nginx/default.conf
scp docker-compose.yml admin@158.160.12.203:/home/admin/docker-compose.yml
scp nginx.conf admin@158.160.12.203:/etc/nginx/conf.d/default.conf

cp default.conf /etc/nginx/conf.d/default.conf

      - ./nginx.conf:/etc/nginx/conf.d/default.conf




home/<ваш_username>/nginx/default.conf