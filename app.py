# Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

## Import and connect Flask Server, connection through local MongoDB

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_function"
mongo = PyMongo(app)

# # Create route for index.html template and finds documents from mongo
@app.route("/")
def home():
    
    #find data
    mars_function = mongo.db.mars_function.find_one()

    #return template and data
    return render_template("index.html", mars_function = mars_function)

#route that triggers scrape function
@app.route("/scrape")
def scrape():

    # Run scrapped functions
    mars_function = mongo.db.mars_function
    mars_data = scrape_mars.mars_function()
    mars_function.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)