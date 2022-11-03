# Проектная работа: диплом

[Репозиторий c дипломной работой](https://github.com/NataliaLaktyushkina/graduate_work)

## Запуск проекта
`docker compose up`
**Статусы платежей:**
- new - платеж создан/отправлен
- in_processing - платеж в обработке (принят), отправлен в процессинг.
- processed - платеж обработан (произошло движение по счетам)
- completed - платеж обработан, отправлено уведомление пользователю
- error  - Ошибка обработки платежа 


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

kafka-console-consumer --bootstrap-server broker:9092 --topic payments --from-beginning

Ctrl-D - exit
