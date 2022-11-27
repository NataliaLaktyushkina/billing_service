FROM python:3.9.12-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY docker/processor/requirements.txt .

RUN apt update && apt install -y netcat && which nc

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY /processor/app /app
COPY /postgresql/db_settings /app/postgresql/db_settings
COPY /postgresql/models /app/postgresql/models
COPY /stripe_app /app/stripe_app
COPY /common /app/common

# create entrypoint for Kafka and ClickHouse waiting
COPY /docker/processor/entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh","/app/entrypoint.sh"]
