from utils.connection import connect_to_consumer
from core.logger import logger
from core.config_saver import settings
from transform import transform_data


async def extract_data() -> None:
    consumer = connect_to_consumer()
    await consumer.start()
    try:
        batch = []
        async for msg in consumer:

            data = {'topic': msg.topic,
                    'key': msg.key,
                    'value': msg.value,
                    'timestamp': msg.timestamp}
            logger.info(msg=data)
            batch.append(data)
            # if len(batch) >= settings.BATCH_SIZE:
            await transform_data(kafka_data=batch)
            # batch = []
    finally:
        await consumer.stop()
