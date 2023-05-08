FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD gunicorn foodgram_django.wsgi:application --bind 0.0.0.0:8000
