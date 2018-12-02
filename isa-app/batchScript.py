# Pulls messages from Kafka and indexes that in ES.
from kafka import KafkaConsumer, KafkaProducer
from kafka.common import NodeNotReadyError
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import json, time

# Attempt to connect to ES and Kafka.
es = Elasticsearch(['es'])

while True:
    try:
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        break
    except NodeNotReadyError:
        time.sleep(1)
        print('Can\'t connect to Kafka, trying again...')
        continue

# Add the data in fixtures to the Kafka queue.
# Code for opening/reading fixture by William Wong, 11/13/18, general Slack channel.
with open('db.json') as fixture:
    fixture_entries = json.load(fixture)
entry_count = 0
for entry in fixture_entries:
    # Only get sample packs from the fixture.
    if entry['model'] == 'microservices.samplepack':
        # Format the entry.
        listing = entry['fields']
        listing['id'] = entry['pk']
        # Index the listing, retrying if necessary.
        while True:
            try:
                es.index(index='listing_index', doc_type='listing', id=listing['id'], body=listing)
                break
            except:
                time.sleep(10)
                print('Elasticsearch is not ready yet, trying again in 10 seconds...')
                continue
        entry_count = entry_count + 1
print('%d listings loaded from fixture...' % entry_count)

# Pull messages from Kafka in real time.
consumer = KafkaConsumer('sample-pack-listings', group_id='listing-indexer', bootstrap_servers=['kafka:9092'], api_version=('0.9'))
for message in consumer:
    # Read the message.
    listing = json.loads((message.value).decode('utf-8'))
    # Index the listing.
    while True:
        try:
            es.index(index='listing_index', doc_type='listing', id=listing['id'], body=listing)
            break
        except:
            time.sleep(10)
            print('Elasticsearch is not ready yet, trying again in 10 seconds...')
            continue
    # Commit the changes.
    es.indices.refresh()
    print('New listing %s added!' % listing['name'])
