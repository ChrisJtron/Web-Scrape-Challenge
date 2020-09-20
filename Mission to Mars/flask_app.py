# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests



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

#create news database
news_db= client.Mars


image_db=client.Mars


# Set route
@app.route('/')
def index():
    # Store the entire team collection in a list
    headlines= (db.headlines.find({}, {'headline': 1}))
    headline=headlines[1]['headline']

    newses=(news_db.news.find_one())
    news=newses['paragraph']
    
    image=(image_db.featured_images.find_one({}, sort=[('_id', pymongo.DESCENDING)]))
    featured_image=image['link']
    print(featured_image)

    # Return the template 
    return render_template('index.html', headline=headline, news=news, featured_image=featured_image)



@app.route('/scrape')
def scrape():
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


    ## Get featured Image
    import time

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    ## click full image button on first page
    full_image_button=browser.find_by_id('full_image')
    full_image_button.click()
    time.sleep(3)

    ##click more info button on second page
    more_info=browser.links.find_by_partial_text('more info')
    more_info.click()
    time.sleep(3)

    #click image
    featured_image=browser.links.find_by_partial_href('/spaceimages/image')
    featured_image.click()

    # get source of image
    featured_link=browser.find_by_tag('img')['src']

    featured_link_dict={}
    featured_link_list=[]
    featured_link_dict['link']=featured_link
    featured_link_list.append(featured_link_dict)





    from flask import Flask, render_template, redirect

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
    #db.headlines.drop()
    # Creates a collection in the database and inserts documents
    db.headlines.insert_one(news_headlines[1])

    #create news database
    news_db= client.Mars
    news_db.news.drop()
    news_db.news.insert_many(news)

    #create a featured_image database
    image_db=client.Mars
    image_db.featured_images.insert_many(featured_link_list)



    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)
