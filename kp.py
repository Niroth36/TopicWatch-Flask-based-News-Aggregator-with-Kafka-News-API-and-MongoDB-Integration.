import requests
from kafka import KafkaProducer
import subprocess
import json

# Set up the Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Set the News API key
api_key = 'f1d9f2f51d3c446eadf7353a460be7e6'

# Set the list of keywords to retrieve articles for
keywords = ['technology', 'business', 'politics', 'science', 'health', 'sports', 'entertainment', 'environment']


def get_articles():
    # Iterate through the keywords
    for keyword in keywords:
        # Use the News API to search for articles with the keyword
        api_url = 'https://newsapi.org/v2/everything'
        params = {
            'q': keyword,
            'apiKey': api_key,
            'pageSize': 100
        }
        r = requests.get(api_url, params=params)
        data = r.json()

        # Get the articles from the response
        articles = data['articles']

        # Send each article to the Kafka topic for its category
        for keyword in keywords:
            # Check if the topic for the category exists
            topic_exists = subprocess.call(['/home/kafka/kafka/kafka_2.12-3.3.1/bin/kafka-topics.sh', '--list', '--bootstrap-server', 'localhost:9092', '--topic', keyword + '-topic']) == 0

            # Create the topic if it does not exist
            if not topic_exists:
                subprocess.call(['/home/kafka/kafka/kafka_2.12-3.3.1/bin/kafka-topics.sh', '--create', '--bootstrap-server', 'localhost:9092', '--replication-factor', '1', '--partitions', '3', '--topic', keyword + '-topic'])

            # Send the article to the topic
            producer.send(keyword + '-topic', json.dumps(articles).encode('utf-8'))

        # Iterate through the articles
        for article in articles:
            # Use the MediaWiki API to search for the source domain
            source_domain = article['source']['name']
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

             # Check if the topic for the category exists
            topic_exists = subprocess.call(['/home/kafka/kafka/kafka_2.12-3.3.1/bin/kafka-topics.sh', '--list', '--bootstrap-server', 'localhost:9092', '--topic', source_domain + '-topic']) == 0

            # Create the topic if it does not exist
            if not topic_exists:
                subprocess.call(['/home/kafka/kafka/kafka_2.12-3.3.1/bin/kafka-topics.sh', '--create', '--bootstrap-server', 'localhost:9092', '--replication-factor', '1', '--partitions', '3', '--topic', source_domain + '-topic'])
            r = requests.get(api_url, params=params)
            data = r.json()

            # Get the description of the first search result
            description = data['query']['search'][0]['snippet']

            # Publish the article to the Kafka topic with the name of the keyword
            producer.send(keyword, value=description.encode())

             # Publish the description to the Kafka topic with the name of the source domain
            producer.send(source_domain, value=description.encode())

            return 'Description published to Kafka topic'

# Run the function to get the articles and publish them to Kafka
get_articles()