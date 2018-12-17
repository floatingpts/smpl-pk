# Pulls messages from Kafka and logs it for Spark to access.
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
consumer = KafkaConsumer('recommendations-log', group_id='recommendations-indexer', bootstrap_servers=['kafka:9092'], api_version=('0.9'))
f = open('data/access.log', 'a')
for message in consumer:
    # Read the message.
    record = json.loads((message.value).decode('utf-8'))
    # Append tab separated values to log.
    user_id = str(record['user_id'])
    listing_id = str(record['listing_id'])
    f.write(user_id + '\t' + listing_id + '\n')
    f.flush()
