from kafka import KafkaProducer
import requests
import time
import subprocess
import json
from app import app

# Set the NewsAPI URL and API key
NEWS_API_URL = 'https://newsapi.org/v2/everything'
NEWS_API_KEY = 'f1d9f2f51d3c446eadf7353a460be7e6'

# Set the list of keywords to retrieve articles for
keywords = ['technology', 'business', 'politics', 'science', 'health', 'sports', 'entertainment', 'environment']

# Set up the Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

@app.route('/get_source_info/<source_domain>')
def get_source_info(source_domain):
    # Use the MediaWiki API to search for the source domain
    api_url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': source_domain,
        'utf8': 1,
        'formatversion': 2,
        'format': 'json'
    }
    r = requests.get(api_url, params=params)
    data = r.json()

    # Get the description of the first search result
    description = data['query']['search'][0]['snippet']

    # Publish the description to the Kafka topic with the name of the source domain
    producer.send(source_domain, value=description.encode())

    return 'Description published to Kafka topic'

# Retrieve and publish articles for each keyword every two hours
while True:
    for keyword in keywords:
        # Make the HTTP request to the NewsAPI
        response = requests.get(NEWS_API_URL, params={
            'q': keyword,
            'apiKey': NEWS_API_KEY
        })

        # Check the status code of the response
        if response.status_code == 200:
            # Parse the response to extract the articles
            articles = response.json()['articles']

            # Send each article to the Kafka topic for its category
            for keyword in keywords:
                # Check if the topic for the category exists
                topic_exists = subprocess.call(['/home/kafka/kafka/kafka_2.12-3.3.1/bin/kafka-topics.sh', '--list', '--bootstrap-server', 'localhost:9092', '--topic', keyword + '-topic']) == 0

                # Create the topic if it does not exist
                if not topic_exists:
                    subprocess.call(['/home/kafka/kafka/kafka_2.12-3.3.1/bin/kafka-topics.sh', '--create', '--bootstrap-server', 'localhost:9092', '--replication-factor', '1', '--partitions', '3', '--topic', keyword + '-topic'])

                # Send the article to the topic
                producer.send(keyword + '-topic', json.dumps(articles).encode('utf-8'))
        else:
            # Print an error message if the request fails
            print('Failed to retrieve articles')

    # Sleep for two hours
    time.sleep(7200)