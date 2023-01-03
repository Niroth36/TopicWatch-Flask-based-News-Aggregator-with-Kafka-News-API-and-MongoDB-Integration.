from kafka import KafkaConsumer
import json
from app import db
import msgpack

# Set the collection


consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         consumer_timeout_ms=1000)

# consume earliest available messages, don't commit offsets
KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# consume msgpack
KafkaConsumer(value_deserializer=msgpack.unpackb)

consumer = KafkaConsumer()

topics = ['technology-topic', 'business-topic', 'politics-topic', 'science-topic', 'health-topic', 'sports-topic', 'entertainment-topic', 'environment-topic']

for topic in topics:
    consumer.subscribe(topic)
    collection = db[topic]
    print(topic)
    for i in range(10):
        message = consumer.poll()
        print(message)
    if message is None:
        print("No message received within 1 second")
    else:
        article = json.loads(str(message))
        print(article)
        # doc = {"title": article["titles"], "description": article["description"], "urlToImage": article["urlToImage"]}
        # collection.insert_one(doc)