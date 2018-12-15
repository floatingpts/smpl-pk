# Pulls messages from Kafka and indexes that in ES.
from kafka import KafkaConsumer, KafkaProducer
from kafka.common import NodeNotReadyError
import json, time

while True:
    try:
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        break
    except NodeNotReadyError:
        time.sleep(1)
        print('Can\'t connect to Kafka, trying again...')
        continue

# Pull messages from Kafka in real time.
consumer = KafkaConsumer('sample-pack-listings', group_id='listing-indexer', bootstrap_servers=['kafka:9092'], api_version=('0.9'))
for message in consumer:
    # Read the message.
    listing = json.loads((message.value).decode('utf-8'))
    print('New listing %s added!' % listing['name'])
