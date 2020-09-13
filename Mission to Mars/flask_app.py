# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests

### Make a list of dictionaries to store in MongDB
## Extract headlines
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url= "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

headlines = soup.find_all('div', class_='content_title')


news_headlines=[]
for headline in headlines:
    headline_data={}
    headline_data['headline']=(headline.text)
    news_headlines.append(headline_data)


##  Extract paragraph text
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url= "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

paragraphs=soup.find_all('div', class_='article_teaser_body')

news=[]    
for par in paragraphs:
    par_data={}
    par_data['paragraph']=(par.text)
    news.append(par_data)




from flask import Flask, render_template

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.Mars
# Drops collection if available to remove duplicates
db.headlines.drop()
# Creates a collection in the database and inserts documents
db.headlines.insert_many(news_headlines)

#create news database
news_db= client.Mars
news_db.news.drop()
news_db.news.insert_many(news)


# Set route
@app.route('/')
def index():
    # Store the entire team collection in a list
    headline= (db.headlines.find_one())
    news=(news_db.news.find_one())

    # Return the template with the teams list passed in
    return render_template('index.html', headline=headline, news=news)


if __name__ == "__main__":
    app.run(debug=True)
