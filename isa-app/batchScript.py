# Pulls messages from Kafka and indexes that in ES
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json, time

# Listen for Kafka messages being added on port 9092.
es = Elasticsearch(['es'])
time.sleep(500)
es.indices.create(index='listing_index')

# Index the data in fixtures for searching.
with open('db.json') as fixture:
    fixture_entries = json.load(fixture)

for entry in fixture_entries:
    if entry['model'] == 'microservices.samplepack':
        body = entry['fields']
        # ID added to search result for convenience in experience layer code.
        body['id'] = entry['pk']

print('%d fixtures loaded.' % len(fixture_entries))

consumer = KafkaConsumer('sample-pack-listings', group_id='listing-indexer', bootstrap_servers=['kafka:9092'], api_version=('0.9'))
time.sleep(500)
# Pull messages from Kafka in real time.
for message in consumer:
    # Read the message.
    listing = json.loads((message.value).decode('utf-8'))
    # Index the listing.
    es.index(index='listing_index', doc_type='listing', id=listing['id'], body=listing)
    # Commit the changes.
    es.indices.refresh()
    print('New listing %s added!' % listing['title'])
