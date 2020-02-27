from flask import Flask, render_template, redirect
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
from flask_pymongo import PyMongo
import os
import pandas as pd
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    data = mongo.db.data.find_one()
    return render_template("index.html",data=data)
    
@app.route("/scrape")
def scraper():
    data = mongo.db.data
    data_content = scrape_mars.scrape()
    data.update({}, data_content, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

