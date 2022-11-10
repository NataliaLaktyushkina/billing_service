#!/bin/sh
set -u

echo "Waiting for Postgresql..."

while ! nc -z postgres 5432; do
  sleep 2
done

echo "Postgresql started"

python main.py
