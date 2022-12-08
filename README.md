# Проектная работа: диплом

[Репозиторий c дипломной работой](https://github.com/NataliaLaktyushkina/graduate_work)

![Схема](scheme/billing_scheme.jpeg)

**Description:**

Пользователь через Subscription API отправляет запрос (payment) на оплату подписки.
Payment добавляется в очередь (Kafka), откуда считывается Saver app.
Saver app все payments кладет в БД (PostgreSQL). Статус платежа = new.
Из БД  Processor вычитывает платежи в статусе new и отправляет их в Processing (Stripe).
Processing производит списание денег и отправляет чек пользователю.

[Auth service](https://github.com/NataliaLaktyushkina/Auth_sprint_2)

[Movie_service](https://github.com/NataliaLaktyushkina/Sprint_4_Async_API)

## Запуск проекта
`docker compose up`

**Alembic:**

Необходимо запустить в папке с файлом *"alembic.ini":*

`alembic revision -m "initial"`

`alembic upgrade head`

`alembic revision --autogenerate -m "create_tables"`

`alembic upgrade head`

**Processing statuses:**
- new - платеж создан/отправлен (subscription_app)
- in_processing - платеж в обработке, отправлен в процессинг (processor)
- completed -  отправлено уведомление пользователю (notification app)
- duplicated - пользователь несколько раз отправил запрос на подписку

**Payment statuses:**
- accepted
- error
- decline
- unknown - новый платеж, либо еще в обработке, либо не получен ответ от процессинга

*ProcessingStatus* - статус платежа в приложении, на этот статус я ориентируюсь, что все действия с платежом выполнены.

*PaymentStatus* - ответ от платежной системы.

Например, может быть ProcessingStatus = completed, PaymentStatus = error.
Это значит, что платеж обработан, но возникли ошибки на стороне платежной системы (например, нет денег или некорректные данные карты).
При такой связке статусов пользователь может еще раз отправить запрос на платеж.
Если же будет ProcessingStatus = completed, PaymentStatus = accepted - значит, платежт прошел успешно, и у пользователя есть активная подписка.


**Переменные окружения:**
- [postgresql](docker/postgres/.env.example)
- [saver](saver/app/core/.env.example)
- [subscription_app](subscription_app/src/core/.env.example)

**Subscription app**:

*http://127.0.0.1:80/api/openapi*

API - позволяет пользователям:
- оплатить подписку,
- посмотреть список своих подписок.
- проверить доступность фильма к просмотру:
  - фильмы с рейтингом выше 7 доступны только по подписке

MOVIE_SERVICE: http://127.0.0.1:90/api/openapi


Администратору:
- Посмотреть список пользователей и их подписок
- Изменить стоимость подписки в БД и в процессинге (stripe)
- Отменить подписку пользователя - на текущий момент этим занимаются адинистраторы,
так как нет четких критeриев от бизнеса, в каком случае пользователь может отменить подписку.

Если у пользователя уже есть подписка, то запрос на платеж не отправляется.

Все запросы от пользователя складываются в очередь (kafka).

![Endpoints](scheme/API.png)

**Saver**:

Считывает платежи из очереди (kafka).
Складывает все платежи в БД (таблица payments) - processing_status = new.

**Processor:**

Отправляет в процессинг (stripe) последний запрос на платеж от пользователя (processing_status = new).
Данные платеж в БД переходит в processing_status = in_processing.

После ответа от stripe:
Платеж в БД переходит в processing_status = completed.
Задублированные запросы от пользователя переходят в  processing_status = duplicated.
Платеж считается дублем, если:
 - от пользователя уже есть запрос на подписку
 - платеж в processing_status = new

Из stripe отправляем пользователю чек об оплате:

https://dashboard.stripe.com/test/payments

Почту пользователя получаем из Auth service:

*AUTH_SERVICE/v1/user_by_id*

**Notification service:** (не реализован)

Если подписка успешно оплачена (processing_status=completed & payment_status=accepted) отправляем еще одно письмо пользователю.

*NOTIFICATION_SERVICE/adminapi/v1/create_mailing*

Письмо пользователю "Спасибо, что оплатили подписку" с подборкой фильмов.

----
**Kafka:**

List of topics inside a container:

`kafka-topics --bootstrap-server broker:9092 --list`

Send message to topic:

`kafka-console-producer --bootstrap-server broker:9092 --topic payments`

kafka-console-consumer --bootstrap-server broker:9092 --topic payments --from-beginning

Ctrl-D - exit
