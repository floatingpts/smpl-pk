# Pulls messages from Kafka and indexes that in ES
from kafka import KafkaConsumer
while True:
    consumer = KafkaConsumer('sample-pack-listings', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
    for message in consumer:
        listing = json.loads((message.value).decode('utf-8'))
        # TODO: How to figure out if listing is new? Does KafkaConsumer do this automatically?
        if listing_is_new:
            # Make request to ElasticSearch container with listing in body
