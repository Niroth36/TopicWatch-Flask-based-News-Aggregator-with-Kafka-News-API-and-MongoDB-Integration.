from flask import Flask, jsonify, request, session, redirect, flash
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
import datetime

class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        print(request.form)

        timestamp = datetime.datetime.now()
        
        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "timestamp": timestamp,
            "city_name": "",
            "keywords": ""
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing email address
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        # MongoDB for users collection
        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def insert_topics(self):
        # Get the user data from the request form
        topics = request.form.getlist('topics')
        email = request.args.get('email')

        # Update mongoDB
        db['users'].update_one({'email': email}, {"$set": {'keywords': topics}})

        return redirect('/dashboard')


    def insert_city(self):
        # Get the user data from the request form
        city = request.form['cityname']
        email = request.args.get('email')

        # Update mongoDB
        db['users'].update_one({'email': email}, {"$set": {'city_name': city}})

        return redirect('/dashboard/')

    def delete_user(self):
        # Delete the user from the MongoDB collection
        email = request.args.get('email')
        db['users'].delete_one({'email': email})

        return redirect('/')

    def login(self):

        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({ "error": "Invalid login credentials"}), 401