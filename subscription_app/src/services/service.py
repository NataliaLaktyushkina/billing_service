import abc
import json

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

from models.payment import Payment


class AbstractPaymentStorage(abc.ABC):

    @abc.abstractmethod
    def send_payment(self, payment: Payment, user_id: str) -> bool:
        pass


class KafkaStorage(AbstractPaymentStorage):
    def __init__(self, producer: AIOKafkaProducer):
        # producer does is enqueue the message on an internal queue which is later
        # (>= queue.buffering.max.ms) served by internal threads and sent to the broker
        self.producer = producer

    async def send_payment(self, payment: Payment, user_id: str) -> bool:
        """Publishes records to the Kafka cluster"""

        # Get cluster layout and initial topic/partition leadership information
        await self.producer.start()

        try:
            # Produce message
            msg = json.dumps(dict(payment), default=str)
            await self.producer.send_and_wait(topic=payment.topic,
                                              value=msg.encode() ,
                                              key=':'.join((user_id, payment.payment_id)).encode())

            payment_was_sent = True
        except KafkaError as error:
            payment_was_sent = False
        finally:
            # Wait for all pending messages to be delivered or expire.
            # Adding flush() before exiting will make the client wait for any outstanding messages
            # to be delivered to the broker
            await self.producer.flush()
        return payment_was_sent
