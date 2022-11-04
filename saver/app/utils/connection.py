import asyncio
import time
from functools import wraps

import aiokafka

from core.config_saver import settings


def backoff(start_sleep_time: float = 0.1,  # type: ignore
            factor: int = 2, border_sleep_time: int = 10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time

    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):   # type: ignore
        @wraps(func)
        def inner(*args, **kwargs):  # type: ignore
            t = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    if t >= border_sleep_time:
                        t = border_sleep_time
                    else:
                        t = start_sleep_time * 2 ^ factor
                    time.sleep(t)

        return inner

    return func_wrapper


@backoff()
def connect_to_consumer() -> aiokafka.AIOKafkaConsumer:
    kafka_settings = settings.kafka_settings
    consumer = aiokafka.AIOKafkaConsumer(
        settings.TOPIC,
        bootstrap_servers=f'{kafka_settings.KAFKA_HOST}:{kafka_settings.KAFKA_PORT}',
        auto_commit_interval_ms=1000,  # Autocommit every second
    )
    return consumer


async def main() -> None:
    consumer = connect_to_consumer()
    await consumer.start()


if __name__ == '__main__':
    asyncio.run(main())
