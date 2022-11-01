# Проектная работа: диплом

[Репозиторий c дипломной работой](https://github.com/NataliaLaktyushkina/graduate_work)

## Запуск проекта
`docker compose up`

**Переменные окружения:**
- [postgresql](docker/postgres/.env.example)
- [saver](saver/app/core/.env.example)

**Processing:**

*http://127.0.0.1:5001/execute_transaction*

[Имитирует](processing/main.py) обращение к внешнему сервису процессинга.
Возвращает ответ - выполнена ли транзакция (success) или нет (error)


**Kafka:**

List of topics inside a container:

`kafka-topics --bootstrap-server broker:9092 --list`

Send message to topic:

`kafka-console-producer --bootstrap-server broker:9092 --topic payments`

Ctrl-D - exit
