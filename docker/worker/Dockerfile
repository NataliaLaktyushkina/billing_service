FROM python:3.9.12-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY docker/worker/requirements.txt .

RUN apt update && apt install -y netcat && which nc

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY /worker/app /app
COPY /postgresql/db_settings /app/postgresql/db_settings

# create entrypoint for Kafka and ClickHouse waiting
COPY /docker/worker/entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh","/app/entrypoint.sh"]
