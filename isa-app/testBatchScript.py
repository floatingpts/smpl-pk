# Pulls messages from Kafka and indexes that in ES
from kafka import KafkaConsumer
import json
consumer = KafkaConsumer('sample-pack-listings', group_id='listing-indexer', bootstrap_servers=['kafka:9092'], api_version=('0.9'))
for message in consumer:
    print("Added to queue!")
    print(json.loads((message.value).decode('utf-8')))
