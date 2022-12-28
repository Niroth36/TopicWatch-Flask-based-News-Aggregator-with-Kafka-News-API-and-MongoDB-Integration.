import json
from flask import Flask, render_template, redirect, session
from functools import wraps
from newsapi import NewsApiClient
from threading import Event
import signal
import requests
from flask_kafka import FlaskKafka
from kafka import KafkaProducer, KafkaConsumer
import pymongo
# from kafka_producer import keywords


app = Flask(__name__)
app.secret_key = b'\xb0\x97\x10\xd2=\xaf\xf1\xe4}t2s\xe6\x94\x91\xb8'

# Connect to the MongoDB database
client = pymongo.MongoClient('localhost', 27017)
db = client['login_user']

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

# Routes
from user import routes

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/bbc/')
def bbc():
    newsapi = NewsApiClient(api_key='f1d9f2f51d3c446eadf7353a460be7e6')
    topheadlines = newsapi.get_top_headlines(sources='bbc-news')

    articles = topheadlines['articles']

    desc = []
    news = []
    img  = []

    for i in range(len(articles)):
        myarticles =  articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])

    mylist = zip(news, desc, img)

    return render_template('bbc.html', context=mylist)

@app.route('/topic/<topic>/')
def topic(topic):
    newsapi = NewsApiClient(api_key='f1d9f2f51d3c446eadf7353a460be7e6')
    everything = newsapi.get_everything(q=topic)

    articles = everything['articles']

    desc = []
    title = []
    img = []

    for i in range(len(articles)):
        myarticles = articles[i]

        title.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])

    mylist = zip(title, desc, img)

    return render_template('topic.html', context=mylist)


# Set up the Kafka consumer to read from the topics and store the data in the MongoDB database
@app.route('/store/')
def store_data():
    # Set up the Kafka consumer
    consumer = KafkaConsumer()

    # Subscribe to the topics
    consumer.subscribe(['technology-topic', 'business-topic', 'politics-topic', 'science-topic', 'health-topic', 'sports-topic', 'entertainment-topic', 'environment-topic'])

    # Read the messages and store them in the MongoDB database
    for message in consumer:
        # Parse the message value as JSON
        article = json.loads(message.value)

        # Insert the article into the MongoDB collection for the category
        db[article['category']].insert_one(article)

if __name__ == "__main__":
    # bus.run()
    # listen_kill_server()
    app.run(debug=True)
