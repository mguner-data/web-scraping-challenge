# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': "/Users/mguner/Downloads/chromedriver_win32/chromedriver.exe"}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    news_title, news_paragraph = marsnews(browser)
    return {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_img_url': jpl(browser),
        'mars_weather': mars_weather(browser),
        'mars_facts': mars_facts(browser),
        'mars_hemispheres': mars_hem(browser)
    }

def marsnews(browser):
    # URL of page to be scraped
    url1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    time.sleep(5)
    
    browser.visit(url1)
    html1=browser.html
    soup1 = bs(html1, 'html.parser')
    # Find the first title
    time.sleep(5)
    news_title = ((soup1.find('ul', class_='item_list')).find('li', class_='slide')).find('div', class_='content_title').text

    
    # Find the first paragrapgh
    time.sleep(5)
    news_paragraph = ((soup1.find('ul', class_='item_list')).find('li', class_='slide')).find('div', class_='article_teaser_body').text

    
    return news_title, news_paragraph

def jpl(browser):
    # URL of page to be scraped
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    # Retrieve page with the requests module
    browser.visit(url2)
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
    # Find the image handle

    img2 = soup2.find('img', class_='main_image')['src']

    featured_image_url =base_url + img2

    return (featured_image_url)

def mars_weather(browser):
    # Twitter and scrape the latest tweet
    url5 = 'https://twitter.com/MarsWxReport/status/1291597742586945538'
    browser.visit(url5)
    time.sleep(5)
    html5 = browser.html
    soup5 = bs(html5, 'html.parser')
    tweets = soup5.find('title').text

    return (tweets)

def mars_facts(browser):
    
    url3 = 'https://space-facts.com/mars/'
    time.sleep(1)
    browser.visit(url3)
    time.sleep(3)
    # html3=browser.html
    # soup3 = bs(html3, 'html.parser')
    tables = pd.read_html(url3)
    df = tables[0]
    df.columns = ['Info', 'Values']
    html_table = df.to_html(index=False, classes='table table-striped')

    return (html_table)

def mars_hem(browser):
    # URL of page to be scraped
    url4 =  'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    time.sleep(5)

    hemisphere_image_urls = []


    browser.visit(url4)
    titles = list(browser.find_by_tag('h3'))

    for i in range(len(titles)):
        
        browser.find_by_tag('h3')[i].click()
        time.sleep(5)
        html4=browser.html
        soup4 = bs(html4, 'html.parser')
        dictionary = {
            'title':soup4.find('h2', class_='title').text,
            'url':soup4.find('div', class_='downloads').find('a')['href']
        }
        hemisphere_image_urls.append(dictionary)
        browser.back()
    browser.quit()

    return hemisphere_image_urls


