import json
from kafka.admin import NewTopic
from kafka import KafkaAdminClient
import os
import django
from channels.layers import get_channel_layer
from aiokafka import AIOKafkaConsumer
import logging
from datetime import datetime

timestamp = datetime.now().isoformat()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dvrc.settings")
django.setup()


def create_kafka_topic(bootstrap_servers='localhost:9092'):
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        topic_list = [
            NewTopic(name='mavlink_messages', num_partitions=1, replication_factor=1),
            NewTopic(name='distance_messages', num_partitions=1, replication_factor=1)
        ]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print('Topics created')
    except Exception as e:
        print(f'Error: {e}')


async def kafka_consumer():
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
            await channel_layer.group_send (
                'mavlink_group',
                {
                    'type':'mavlink_message',
                    'topic': message.topic,
                    'data': message.value
                }
            )
    finally:
        await consumer.stop()


logger = logging.getLogger('myapp')
logger.setLevel(logging.WARNING)

if not logger.handlers:
    handler = logging.FileHandler('kafka_log.log', encoding='utf-8')
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)



