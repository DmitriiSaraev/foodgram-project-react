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