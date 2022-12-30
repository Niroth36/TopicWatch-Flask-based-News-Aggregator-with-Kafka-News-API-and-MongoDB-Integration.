from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Set up the Kafka consumer
consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

# Set up the MongoDB client
client = MongoClient('mongodb://localhost:27017/')

# Set the database and collection
db = client['database']
collection = db['collection']

# Subscribe to the topics
consumer.subscribe(['technology-topic', 'business-topic', 'politics-topic', 'science-topic', 'health-topic', 'sports-topic', 'entertainment-topic', 'environment-topic', 'sources domain name'])

# Consume the messages
for message in consumer:
    # Insert the message into the collection
    collection.insert_one(message.value)