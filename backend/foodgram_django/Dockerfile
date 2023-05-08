FROM python:3.7-slim

WORKDIR /app

COPY ./ .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram_django.foodgram_django.wsgi:application", "--bind", "0:8000" ]