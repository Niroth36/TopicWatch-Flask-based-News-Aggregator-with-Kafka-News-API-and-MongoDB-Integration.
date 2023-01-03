from flask import Flask, render_template
from app import app
from app import db

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