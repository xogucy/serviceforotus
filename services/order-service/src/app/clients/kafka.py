from aiokafka import AIOKafkaProducer

from app.modules.schemas import OrderPaymentResultEvent


class OrderPaymentResultPublisher:
    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic

    async def publish(self, event: OrderPaymentResultEvent) -> None:
        producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda value: value.encode("utf-8"),
            enable_idempotence=True,
        )

        await producer.start()
        try:
            await producer.send_and_wait(
                self.topic,
                event.model_dump_json(),
                key=str(event.data.orderId).encode("utf-8"),
            )
        finally:
            await producer.stop()
