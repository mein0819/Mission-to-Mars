from flask import Flask, render_template #redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# set up home page route

#display home page
@app.route("/")

# function to link web app to code that powers it
def index():
    # use PyMongo to find 'mars' collection in database, assign path to variable
    mars = mongo.db.mars.find_one()
    # tell Flask to return an html template, use the mars collection in MongoDB
    return render_template("index.html", mars = mars)

# set up scaping route

# define route
@app.route("/scrape")

#function to access database, scrape new data, update database, return message
def scrape():
   # variable that points to mongo database 
   mars = mongo.db.mars
   # variable to hold newly scraped data, reference function from scraping.py file
   mars_data = scraping.scrape_all()
   # update database, create new document if one doesn't exist
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   # redirect back to homepage to see updated content
   return redirect('/', code=302)

# code to tell flask to run
if __name__ == "__main__":
   app.run()