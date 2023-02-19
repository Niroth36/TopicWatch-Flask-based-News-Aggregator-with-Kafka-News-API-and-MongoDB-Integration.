import requests
import time
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092')
topics = ['technology', 'business', 'politics', 'science', 'health', 'sports', 'entertainment', 'environment']

NEWS_API_URL = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "f1d9f2f51d3c446eadf7353a460be7e6"


def get_and_send_articles(topic):
    params = {
        "q": topic,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        articles = response.json()["articles"]
        for article in articles:
            producer.send(topic + '-topic', value=json.dumps(article).encode('utf-8'))
            print(f"Sent article with title '{article['title']}' to topic '{topic}'")
    else:
        print(f"Failed to fetch articles for topic '{topic}': {response.text}")


while True:
    for topic in topics:
        get_and_send_articles(topic)

    time.sleep(20)  # wait 2 hours before making the next request
