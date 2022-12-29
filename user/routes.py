from flask import Flask
from app import app
from user.models import User

@app.route('/user/signup/', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/delete_user')
def delete_user():
    return User().delete_user()

@app.route('/insert_city', methods=['POST'])
def insert_city():
    return User().insert_city()

@app.route('/insert_topics', methods=['POST'])
def insert_topics():
    return User().insert_topics()

@app.route('/user/login', methods=['POST'])
def login():
    return User().login()