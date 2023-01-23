import subprocess
import json
from app import db
from kafka import KafkaConsumer
import msgpack
import time

consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         consumer_timeout_ms=1000)

# consume earliest available messages, don't commit offsets
KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# consume msgpack
KafkaConsumer(value_deserializer=msgpack.unpackb)

consumer = KafkaConsumer()

topics = ['technology-topic', 'business-topic', 'politics-topic', 'science-topic', 'health-topic', 'sports-topic', 'entertainment-topic', 'environment-topic']

def consume_msg(topic):
    collection = db[topic]
    # Start the Kafka consumer using the subprocess module
    process = subprocess.Popen(["/home/kafka/kafka/kafka_2.12-3.3.1/bin/kafka-console-consumer.sh",
                                "--bootstrap-server", "localhost:9092",
                                "--topic", topic,
                                "--partition", "0",
                                "--offset", "0"],
                            stdout=subprocess.PIPE)

    # Continuously read the output of the consumer and insert the data into the MongoDB collection
    for i in range(10):
        line = process.stdout.readline()
        if not line:
            break
        data = json.loads(line.decode('utf-8').strip())
        collection.replace_one({}, data, upsert=True)

    # Close the consumer and the MongoDB connection
    process.kill()

while True:
    for topic in topics:
        consume_msg(topic)
    time.sleep(7200)