#!/bin/sh
set -u

echo "Waiting for Kafka..."

while ! nc -z broker 29092; do
  sleep 2
done

echo "Kafka started"

python main.py
