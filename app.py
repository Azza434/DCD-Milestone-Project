import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'vehicle_log'
app.config["MONGO_URI"] = "mongodb+srv://root:64XxzJZr7uXrfwyy@myfirstcluster-pffgj.mongodb.net/vehicle_log?retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_data')
def get_data():
    return render_template("data.html", info=mongo.db.info.find())


app.run(host=os.getenv("IP", "0.0.0.0"),
        port=(os.getenv("PORT", "5000")), debug=False)