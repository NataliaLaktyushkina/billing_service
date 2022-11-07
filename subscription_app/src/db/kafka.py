from typing import Optional

from aiokafka import AIOKafkaProducer

bus_kafka: Optional[AIOKafkaProducer] = None


async def get_kafka() -> AIOKafkaProducer:
    return bus_kafka
