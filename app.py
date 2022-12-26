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


@app.route('/bbc')
def index():
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

    return render_template('index.html', context=mylist)

@app.route('/topic/<topic>')
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


if __name__ == "__main__":
    # bus.run()
    # listen_kill_server()
    app.run(debug=True)
