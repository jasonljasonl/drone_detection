from django.core.management.base import BaseCommand
import asyncio
from aiokafka import AIOKafkaConsumer
import json
from channels.layers import get_channel_layer

class Command(BaseCommand):
    help = "Run Kafka consumer"

    def handle(self, *args, **kwargs):
        asyncio.run(self.consume())

    async def consume(self):
        consumer = AIOKafkaConsumer(
            'mavlink_messages',
            'distance_messages',
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        await consumer.start()
        channel_layer = get_channel_layer()
        try:
            async for message in consumer:
                print(f'{message.topic}: {message.value}')
                await channel_layer.group_send(
                    'mavlink_group',
                    {
                        'type':'mavlink_message',
                        'topic': message.topic,
                        'data': message.value
                    }
                )
        finally:
            await consumer.stop()
