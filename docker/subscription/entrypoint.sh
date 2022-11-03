#!/bin/sh

echo "Waiting for Kafka..."

while ! nc -z broker 29092; do
  sleep 2
done

echo "Kafka started"

gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8101 main:app

