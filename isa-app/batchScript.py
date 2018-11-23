from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

#consumer listens to see if any listings added to Kafka queue
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])

#used to add listings to elastic search index
es = Elasticsearch(['es'])

for message in consumer:
    # add listing to elastic search
    es.index(index='listing_index', doc_type='listing', id=message['id'], body=message)
{'created': True, '_version': 1, '_shards': {'successful': 1, 'total': 2, 'failed': 0}, '_index': 'listing_index', '_id': '42', '_type': 'listing'}
    es.indices.refresh(index="listing_index")
