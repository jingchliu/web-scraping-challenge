from flask import Flask, render_template
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
from flask_pymongo import PyMongo
import os
import pandas as pd

def scrape():
    data={}
    news_url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response1 = requests.get(news_url)
    soup1 = bs(response1.text, 'lxml')
    results1 = soup1.body.find("div", class_="slide")
    news_title=results1.find('div',class_='content_title').text
    news_p=results1.find('div',class_="rollover_description_inner").text
    data['news_title']=news_title
    data['news_p']=news_p

    image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_image_url='https://www.jpl.nasa.gov'
    response2 = requests.get(image_url)
    soup2 = bs(response2.text, 'lxml')
    featured_image= soup2.body.find("article", class_="carousel_item")['style']
    featured_image=featured_image.replace("background-image: url('","")
    featured_image=featured_image.replace("');","")
    featured_image_url=base_image_url+featured_image
    data['featured_image_url'] = featured_image_url

    weather_url='https://twitter.com/marswxreport?lang=en'
    response3 = requests.get(weather_url)
    soup3 = bs(response3.text, 'lxml')
    tweet=soup3.body.find("li", {"data-item-type": "tweet"})
    tweet_text_box = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    images_in_tweet_tag = tweet_text_box.find_all("a", {"class": "twitter-timeline-link u-hidden"})
    tweet_text = tweet_text_box.text
    for image_in_tweet_tag in images_in_tweet_tag:
        mars_weather = tweet_text.replace(image_in_tweet_tag.text, '')
    data['mars_weather'] = mars_weather

    fact_url='https://space-facts.com/mars/'
    tables=pd.read_html(fact_url)
    df=tables[0]
    df.rename(columns={ df.columns[0]: "Description" }, inplace = True)
    df.rename(columns={ df.columns[1]: "Value" }, inplace = True)
    df.set_index('Description',inplace=True)
    df.to_html('table.html')
    soup_table = bs(open("table.html"), "html.parser")
    print("Soup Table Type", type(soup_table))
    th=[]
    td=[]
    for x in range(9):
        th.append(soup_table.tbody.find_all('th')[x].text)
        td.append(soup_table.tbody.find_all('td')[x].text)
    table_title_1=soup_table.find_all('th')[1].text
    table_title_2=soup_table.find_all('th')[2].text
    data ['table_title_1'] = table_title_1
    data ['table_title_2'] = table_title_2
    data['th']=th
    data['td']=td

    hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(hemisphere_url)
    hemisphere_image_urls=[]
    html=browser.html
    for x in range(1,5):
        browser.click_link_by_partial_text('Enhanced')
        soup=bs(browser.html,'html.parser')
        #print('New HTML', browser.html)
        title=soup.find('h2',class_='title').text.replace(' Enhanced','')
        # print('New Title', type(title))
        img_url=soup.find('div',class_='downloads').find('a')['href']
        list={
            'title':title,
            'img_url':img_url
        }
        hemisphere_image_urls.append(list)
    data['hemisphere_image_urls'] = hemisphere_image_urls
    return data