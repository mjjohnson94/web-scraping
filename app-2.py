from http import client
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route('/')
def home(): 

    mars_db = mongo.db.mars
    data=mars_db.find_one()
    return render_template('index.html', mars_data=data)

@app.route('/scrape')                                                                                                                                                                                                                                                                                                 
def scrape_all(): 

    mars_db = mongo.db.mars
    scrape_data=scrape_mars.scrape_all()
    mars_db.update({}, scrape_data, upsert=True)

    return redirect("/")

if __name__=='__main__': 
    app.run(debug=True, port=2939)


