#!/usr/bin/env python
import os
import pymongo
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

MONGO_URL = 'mongodb://heroku_pp4rkrx5:9919l2jg2bmm0jrvf50oj8m3f3@ds141613.mlab.com:41613/heroku_pp4rkrx5?retryWrites=false'
client = MongoClient(MONGO_URL)
db = client.heroku_pp4rkrx5
collection = db.shoutouts
app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
	shouts = collection.find()
	return render_template('index.html', shouts=shouts)


@app.route("/post", methods=['POST'])
def post():
	shout = {"name": request.form['name'], "message": request.form['message']}
	shout_id = collection.insert_one(shout) 
	return redirect('/')

@app.route("/db", methods=["Get"])
def database():
	print(db)
	return redirect('/')


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
