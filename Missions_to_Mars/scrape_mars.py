from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import os
import pandas as pd

def scrape():
    news_url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response1 = requests.get(news_url)
    soup1 = bs(response1.text, 'lxml')
    results1 = soup1.body.find("div", class_="slide")
    news_title=results1.find('div',class_='content_title').text
    news_p=results1.find('div',class_="rollover_description_inner").text

    image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_image_url='https://www.jpl.nasa.gov'
    response2 = requests.get(image_url)
    soup2 = bs(response2.text, 'lxml')
    featured_image= soup2.body.find("article", class_="carousel_item")['style']
    featured_image=featured_image.replace("background-image: url('","")
    featured_image=featured_image.replace("');","")
    featured_image_url=base_image_url+featured_image

    weather_url='https://twitter.com/marswxreport?lang=en'
    response3 = requests.get(weather_url)
    soup3 = bs(response3.text, 'lxml')
    tweet=soup3.body.find("li", {"data-item-type": "tweet"})
    tweet_text_box = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    images_in_tweet_tag = tweet_text_box.find_all("a", {"class": "twitter-timeline-link u-hidden"})
    tweet_text = tweet_text_box.text
    for image_in_tweet_tag in images_in_tweet_tag:
        mars_weather = tweet_text.replace(image_in_tweet_tag.text, '')

    fact_url='https://space-facts.com/mars/'
    tables=pd.read_html(fact_url)
    df=tables[0]
    df.rename(columns={ df.columns[0]: "Description" }, inplace = True)
    df.rename(columns={ df.columns[1]: "Value" }, inplace = True)
    df.set_index('Description',inplace=True)
    html_table=df.to_html

    hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_hemisohere_url='https://astrogeology.usgs.gov/'
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(hemisphere_url)
    hemisphere_image_urls=[]
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    descriptions=soup.find_all('div',class_='item')
    descriptions
    for description in descriptions:
        title=description.find('h3').text.replace(' Enhanced','')
        img_url=description.find('img',class_='thumb')['src']
        list={
            'title':title,
            'img_url':base_hemisohere_url+img_url
        }
        hemisphere_image_urls.append(list)

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/scrape")
def scraper():
    return render_template("index.html", news_title=news_title, news_p=news_p)
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=True)

