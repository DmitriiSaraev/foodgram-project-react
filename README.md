# praktikum_new_diplom
## Продуктовый помощник.
http://158.160.18.181/

Сайт на котором пользователи публикуют свои рецепты, 
Пользователь региструется и у него появляется возможность публиковать
рецепты, редактировать их, смотреть и добавлять в избранное рецепты 
других пользователей, подписываться на других пользоваелей,
скачать список ингредиентов для приготовления рецептов которые
добавлены в избренное.

## Запуск проекта

Создать ВМ:
прописать имя ВМ
выбрать Ubuntu 20.04
прописать Логин
прописать SSH-ключ  для его получения 
в командной строке ввести:

```cat ~/.ssh/id_rsa.pub```

Подключение к ВМ:
в терминале ввести:  
```ssh admin@158.160.2.202```

admin - это логин который прописали при создании ВМ
IP - тот что выдали когда ВМ создалась (Публичный IPv4)

Ввести команды:

```sudo apt update```

```sudo apt upgrade -y```


Устрановка nginx:

```sudo apt install nginx -y``` 

```sudo ufw allow 'Nginx Full'```

```sudo ufw allow OpenSSH```

```sudo ufw enable```

Проверить сработало ли:

```sudo ufw status```

Если Status: inactive то повторить: 

```sudo ufw enable```

Остановить nginx если запущен

```sudo systemctl stop nginx```

Установить Докер

```sudo apt install docker.io``` 

Установите docker-compose
Проверить версию можно тут:

```https://github.com/docker/compose/releases```

Установить docker-compose:
```sudo curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose```

Затем необходимо задать правильные разрешения, чтобы сделать команду docker-compose исполняемой:

```sudo chmod +x /usr/local/bin/docker-compose```

Чтобы проверить успешность установки, запустите следующую команду:

```docker-compose --version```

Скопируйте файлы docker-compose.yaml и nginx/default.conf
из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml 
и home/<ваш_username>/nginx.conf соответственно.

```scp docker-compose.yml admin@158.160.18.181:/home/admin/docker-compose.yml```

```scp nginx.conf admin@158.160.18.181:/home/admin/nginx.conf```

Далее пушим на Гит
Создаем миграции:
```sudo docker-compose exec backend python manage.py makemigrations```

Проводим миграции:

```sudo docker-compose exec backend python manage.py migrate```

Собираем статику для админки:

```sudo docker-compose exec backend python manage.py collectstatic --no-input```

Если все сделано верно то проект взлетел по вашему IP или домену.

Далее не много справочной информации

посмотреть все контейнеры:

```sudo docker ps -a```

посмотреть запущенные контейнеры:

```sudo docker ps```

посмотреть логи:

```sudo docker logs 69db66638e69```


Установить зависимости:

```pip install -r requirements.txt``` 

Создать файл зависимостей:

```pip freeze > requirements.txt```


DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 


