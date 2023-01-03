from kafka import KafkaConsumer
from pymongo import MongoClient
import json
from app import db
import subprocess

# Set up the Kafka consumer
consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         consumer_timeout_ms=1000)

bootstrap_server = 'localhost:9092'
topic = 'technology-topic'

# Subscribe to the topics
# consumer.subscribe(['technology-topic', 'business-topic'])
# , 'business-topic', 'politics-topic', 'science-topic', 'health-topic', 'sports-topic', 'entertainment-topic', 'environment-topic', 'sources domain name'

# Set the collection
collection = db['collection']

# Use the subprocess module to call the kafka-console-consumer.sh script
consumer = subprocess.Popen(['/home/kafka/kafka/kafka_2.12-3.3.1/bin/kafka-console-consumer.sh',
                                  '--bootstrap-server', bootstrap_server,
                                  '--topic', topic, '--partition', '0','--offset', '0'], 
                                  stdout=subprocess.PIPE)

# Consume the messages
for i in range(10):
    # Process the message
    line = next(consumer.stdout)
    message = line.decode('utf-8').strip()
    print(message)

# Close the consumer
consumer.terminate()

# # Consume the messages
# for message in consumer:
#     print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
#                                           message.offset, message.key,
#                                           message.value))
#     # Insert the message into the collection
#     collection.insert_one(message.value)
    