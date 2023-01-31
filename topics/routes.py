from flask import Flask, render_template, request, send_file
from app import app
from app import db
import networkx as nx
from bson import ObjectId
import matplotlib.pyplot as plt
from graphviz import Digraph
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.readwrite import json_graph
from io import BytesIO
import base64
from dateutil.relativedelta import relativedelta
import datetime
from datetime import datetime, timedelta
import pandas as pd

# Technology-topic
technology_collection = db['technology-topic']

# Find all documents in the collection
technology_docs = technology_collection.find().limit(10)

@app.route('/technology/')
def technology():
    technology_docs = technology_collection.find().limit(10)
    return render_template('technology.html', technology_docs=technology_docs)

# Business-topic
business_collection = db['business-topic']

# Find all documents in the collection
business_docs = business_collection.find().limit(10)

@app.route('/business/')
def business():
    business_docs = business_collection.find().limit(10)
    return render_template('business.html', business_docs=business_docs)

# Politics-topic
politics_collection = db['politics-topic']

# Find all documents in the collection
politics_docs = politics_collection.find().limit(10)

@app.route('/politics/')
def politics():
    politics_docs = politics_collection.find().limit(10)
    return render_template('politics.html', politics_docs=politics_docs)

# Science-topic
science_collection = db['science-topic']

# Find all documents in the collection
science_docs = science_collection.find().limit(10)

@app.route('/science/')
def science():
    science_docs = science_collection.find().limit(10)
    return render_template('science.html', science_docs=science_docs)

# Health-topic
health_collection = db['health-topic']

# Find all documents in the collection
health_docs = health_collection.find().limit(10)

@app.route('/health/')
def health():
    health_docs = health_collection.find().limit(10)
    return render_template('health.html', health_docs=health_docs)

# Sports-topic
sports_collection = db['sports-topic']

# Find all documents in the collection
sports_docs = sports_collection.find().limit(10)

@app.route('/sports/')
def sports():
    sports_docs = sports_collection.find().limit(10)
    return render_template('sports.html', sports_docs=sports_docs)

# Entertainment-topic
entertainment_collection = db['entertainment-topic']

# Find all documents in the collection
entertainment_docs = entertainment_collection.find().limit(10)

@app.route('/entertainment/')
def entertainment():
    entertainment_docs = entertainment_collection.find().limit(10)
    return render_template('entertainment.html', entertainment_docs=entertainment_docs)

# Environment-topic
environment_collection = db['environment-topic']

# Find all documents in the collection
environment_docs = environment_collection.find().limit(10)

@app.route('/environment/')
def environment():
    environment_docs = environment_collection.find().limit(10)
    return render_template('environment.html', environment_docs=environment_docs)
 

@app.route('/graph/', methods=['POST'])
def graph():
    article_id = request.form['article_id']
    topic = request.args.get('topic')
    collection = db[topic+'-topic']
    article = collection.find_one({"_id": ObjectId(article_id)})

    # Build the graph
    G = nx.Graph() 

    # Create a node for the article
    nodes = G.add_node(article['title'], label=article['title'], title=article['title'],
             url=article['url'], author=article['author'])

    # Get all the articles in the same topic
    articles = list(collection.find())        
    article_time_diff = {}
        
    index = 0

    # Add edges between articles that share the same author or source
    for art1 in articles:
        for art2 in articles:
            if art1['_id'] != art2['_id']:
                if art1['author'] == art2['author'] or art1['source']['name'] == art2['source']['name']:
                    if art1['_id'] == ObjectId(article_id) or art2['_id'] == ObjectId(article_id):
                        G.add_edge(art1['title'], art2['title'])
                        index += 1
                else:
                    date1 = datetime.strptime(art1['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                    date2 = datetime.strptime(art2['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                    diff = relativedelta(date1, date2)
                    if art1['_id'] == ObjectId(article_id):
                        article_time_diff[art2['title']] = abs(diff.days)
                    elif art2['_id'] == ObjectId(article_id):
                        article_time_diff[art1['title']] = abs(diff.days)
                    
                        
    if index == 0:
        recommended_article = sorted(article_time_diff, key=article_time_diff.get)[0]
        G.add_edge(article['title'], recommended_article)
    else:
        # Calculate the degree centrality of each node in the graph
        degree_centrality = nx.degree_centrality(G)

        # Sort the degree centrality values in descending order
        sorted_degree_centrality = dict(sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True))

        # Get the first article from the sorted list of degree centralities
        recommended_article = list(sorted_degree_centrality.keys())[1]
        G.clear()
        G.add_edge(article['title'], recommended_article)

    pos = graphviz_layout(G, prog='dot')

    # print(article_time_diff)

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", alpha=0.5)

    img = BytesIO() # file-like object for the image
    plt.savefig(img) # save the image to the stream
    img.seek(0) # writing moved the cursor to the end of the file, reset
    plt.clf() # clear pyplot

    img_data = base64.b64encode(img.getvalue()).decode()

    return render_template('graph.html', img_data=img_data, recommended_article=recommended_article)


@app.route("/stackedbar")
def plot_stacked_bar():

    # List of topics
    topics = ['technology', 'business', 'politics', 'science', 'health', 'sports', 'entertainment', 'environment']

    five_days_ago = datetime.now() - timedelta(days=5)

    topic_counts = {}
    for topic in topics:
        collection = db[topic+'-topic']
        articles = collection.find({'publishedAt': {'$exists': True}})
        for article in articles:
            if datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ') > five_days_ago:
                if topic in topic_counts:
                    topic_counts[topic] += 1
                else:
                    topic_counts[topic] = 1

    topics = list(topic_counts.keys())
    counts = list(topic_counts.values())

    colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink', 'gray']
    fig = plt.figure(figsize=(12, 7))
    for i, topic in enumerate(topics):
        plt.bar(topic, counts[i], color=colors[i])
    plt.xlabel('Topics')
    plt.ylabel('Number of articles')
    plt.title('Stacked bar plot of recent articles by topic')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_data = base64.b64encode(img.getvalue()).decode('utf-8')
    
    return render_template('stackedbar.html', img_data=img_data)

