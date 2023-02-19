import subprocess
import json
from app import db
from kafka import KafkaConsumer
import msgpack
import time
from neo4j import GraphDatabase

consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         consumer_timeout_ms=1000)

# consume earliest available messages, don't commit offsets
KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# consume msgpack
KafkaConsumer(value_deserializer=msgpack.unpackb)

consumer = KafkaConsumer()

topics = ['technology-topic', 'business-topic', 'politics-topic', 'science-topic', 'health-topic', 'sports-topic', 'entertainment-topic', 'environment-topic']

# Neo4j connection settings
neo4j_uri = "neo4j://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "3663"

# Create the Neo4j driver
neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

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
    data = []
    with neo4j_driver.session() as neo4j_session:
        for i in range(100):
            line = process.stdout.readline()
            if not line:
                break
            data.append(json.loads(line.decode('utf-8').strip()))
            neo4j_session.run(
            "CREATE (n: Topic {topic: $topic, source_name: $source_name, title: $title, author: $author, description: $description, url: $url, urlToImage: $urlToImage, publishedAt: $publishedAt, content: $content})",
            topic = topic,
            source_name=data[i]['source']['name'],
            title=data[i]['title'],
            author=data[i]['author'],
            description=data[i]['description'],
            url=data[i]['url'],
            urlToImage=data[i]['urlToImage'],
            publishedAt=data[i]['publishedAt'],
            content=data[i]['content']
            )



        collection.insert_many(data)
        # print(data)
           
    process.kill()

while True:
    for topic in topics:
        consume_msg(topic)
    time.sleep(20)