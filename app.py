import json
from flask import Flask, render_template, redirect, session, jsonify
from functools import wraps
from newsapi import NewsApiClient
from threading import Event
import signal
import requests
from flask_kafka import FlaskKafka
from kafka import KafkaProducer, KafkaConsumer
import pymongo
from py2neo import Graph, Node
from neo4j import GraphDatabase

app = Flask(__name__)
app.secret_key = b'\xb0\x97\x10\xd2=\xaf\xf1\xe4}t2s\xe6\x94\x91\xb8'

uri = "neo4j://localhost:7687"
neo4j_driver = GraphDatabase.driver(uri, auth=("neo4j", "3663"))

@app.route("/create-person")
def create_person():
    with neo4j_driver.session() as neo4j_session:
        neo4j_session.run("CREATE (:Person {name: 'Alice'})")

    return jsonify({"status": "success"})

data = {
    "_id" : "63d92d5cef5359682e806883",
    "source" : {
        "id" : None,
        "name" : "NPR"
    },
    "author" : "The Associated Press",
    "title" : "West Virginia can keep its ban against transgender school athletes, a judge says",
    "description" : "The judge said he recognized that being transgender is \"natural\" and \"not a choice.\" But he said one's sex is also natural and \"dictates physical characteristics that are relevant to athletics.\"",
    "url" : "https://www.npr.org/2023/01/06/1147361439/west-virginia-transgender-sports-ban",
    "urlToImage" : "https://media.npr.org/include/images/facebook-default-wide-s1400-c100.jpg",
    "publishedAt" : "2023-01-06T14:34:50Z",
    "content" : "CHARLESTON, W.Va. West Virginia's ban on transgender athletes competing in female school sports is constitutional and can remain in place, a federal judge ruled Thursday.\r\n\"I recognize that being tra… [+3331 chars]"
}

@app.route("/create-topic")
def create_topic():
    with neo4j_driver.session() as neo4j_session:
        neo4j_session.run(
        "CREATE (t:Topic {title: $title, author: $author, description: $description, url: $url, urlToImage: $urlToImage, publishedAt: $publishedAt, content: $content})",
        title=data['title'],
        author=data['author'],
        description=data['description'],
        url=data['url'],
        urlToImage=data['urlToImage'],
        publishedAt=data['publishedAt'],
        content=data['content']
    )

    return jsonify({"status": "success"})

@app.route("/clear-nodes")
def clear_nodes():
    with neo4j_driver.session() as neo4j_session:
        neo4j_session.run("MATCH (n) DETACH DELETE n")

    return jsonify({"status": "success"})

# Connect to the MongoDB database
client = pymongo.MongoClient('localhost', 27017)
db = client['mongoDB']

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
from topics import routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/news/')
def news():
    return render_template('news.html')

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
    url = []
    img = []

    for i in range(len(articles)):
        myarticles = articles[i]

        title.append(myarticles['title'])
        desc.append(myarticles['description'])
        url.append(myarticles['url'])
        img.append(myarticles['urlToImage'])

    mylist = zip(title, desc,url, img)

    return render_template('topic.html', context=mylist)


if __name__ == "__main__":
    # bus.run()
    # listen_kill_server()
    app.run(debug=True)
