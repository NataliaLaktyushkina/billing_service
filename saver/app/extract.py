from core.logger import logger
from transform import transform_data
from utils.connection import connect_to_consumer


async def extract_data() -> None:
    consumer = connect_to_consumer()
    await consumer.start()
    try:
        async for msg in consumer:

            data = {'topic': msg.topic,
                    'key': msg.key,
                    'value': msg.value,
                    'timestamp': msg.timestamp}
            logger.info(msg=data)
            await transform_data(kafka_data=[data])
    finally:
        await consumer.stop()
