import json
from flask import Flask, render_template
from newsapi import NewsApiClient
from threading import Event
import signal
import requests
from flask_kafka import FlaskKafka
from kafka import KafkaProducer, KafkaConsumer

from kafka_producer import topics


app = Flask(__name__)

ENDPOINT = 'https://newsapi.org/v2/everything?q=tesla&from=2022-11-13&sortBy=publishedAt&apiKey=f1d9f2f51d3c446eadf7353a460be7e6'
API_KEY = 'f1d9f2f51d3c446eadf7353a460be7e6'


producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

topic = topics


def send_message(topic, message):
    producer.send(topic, message)


consumer = KafkaConsumer('my-topic',
                        bootstrap_servers = ['localhost:9092'],
                        auto_offset_reset='earliest',
                        group_id = 'my-group',
                        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer.flush()

@app.route('/consumer')
def consumer():
    messages = []
    for message in consumer:
        messages.append(message.value)
    return render_template('consumer.html', messages=messages)

INTERRUPT_EVENT = Event()

bus = FlaskKafka(INTERRUPT_EVENT, 
                bootstrap_servers=",".join(["localhost:9092"]),
                group_id="consumer-grp-id"
                )


def listen_kill_server():
    signal.signal(signal.SIGTERM, bus.interrupted_process)
    signal.signal(signal.SIGTERM, bus.interrupted_process)
    signal.signal(signal.SIGTERM, bus.interrupted_process)
    signal.signal(signal.SIGTERM, bus.interrupted_process)

@bus.handle('test-topic')
def test_topic_handler(msg):
    print("consumed {} from test-topic".format(msg))

@app.route('/bbc')
def bbc():
    newsapi = NewsApiClient(api_key="f1d9f2f51d3c446eadf7353a460be7e6")
    topheadlines = newsapi.get_top_headlines(sources="bbc-news")

    articles = topheadlines['articles']

    desc = []
    news = []
    img = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])

    mylist = zip(news, desc, img)

    return render_template('index.html', context=mylist)

# Define the Flask route for the news API
@app.route('/news')
def get_news():
    # Set the NewsAPI URL and API key
    NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'
    NEWS_API_KEY = 'f1d9f2f51d3c446eadf7353a460be7e6'

    # Get the topic from the request query string
    # topic = request.args.get('topic')
    topic = 'technology'

    # Make the HTTP request to the NewsAPI
    response = requests.get(NEWS_API_URL, params={
        'q': topic,
        'apiKey': NEWS_API_KEY
    })

    # Check the status code of the response
    if response.status_code == 200:
        # Parse the response to extract the articles
        articles = response.json()['articles']

        # Return the articles as a JSON response
        return articles
    else:
        # Return an error message if the request fails
        return 'Failed to retrieve articles', response.status_code



@app.route('/')
def index():
    # Replace with your search parameters
    params = {
        'api-key': API_KEY,
        'q': 'tesla'
    }


    response = requests.get(ENDPOINT, params=params)
    articles = response.json()['response']['docs']

    for article in articles:
            producer.send('my-topic', article)
    return 'Articles sent to Kafka'

if __name__ == "__main__":
    bus.run()
    listen_kill_server()
    app.run(debug=True)
