from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import script

app = Flask(__name__)

# setup mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    all_data = mongo.db.all_data.find_one()
    print(all_data)    

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", mars=all_data)

@app.route("/scrape")
def scrape():
  
    mongo_dict = script.scrape_info()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.all_data.update({}, mongo_dict, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)