FROM python:3.9-slim


ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENV PYTHONPATH="/app"
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./weather_analyzer /app/

RUN chmod +x /app/entrypoint.sh