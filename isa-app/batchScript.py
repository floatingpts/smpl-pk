# Pulls messages from Kafka and indexes that in ES
from kafka import KafkaConsumer
while True:
    consumer = KafkaConsumer('sample-pack-listings', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
    # Exception handling with Docker Compose
    for message in consumer:
        listing = json.loads((message.value).decode('utf-8'))

