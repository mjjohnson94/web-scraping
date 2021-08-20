# Importing dependencies:

from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser, browser
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd 

### Initializing the browser:

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=True)

### Scraping the webpage for the latest news headline:

def scrape_headline(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')

    result = soup.find_all("div", class_="content_title")[0]
    news_headline = result.text

    return news_headline

### Scraping the webpage for the corresponding news paragraph:

def scrape_paragraph(browser):

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')

    paragraph = soup.find_all("div", class_="article_teaser_body")[0]
    news_paragraph = paragraph.text.strip()

    return news_paragraph

#### Using the Pandas library to scape a table containing Mars Facts from the webpage:

def data_frame():

    data_table = pd.read_html('https://galaxyfacts-mars.com/')
    data = data_table[0]

    df = pd.DataFrame(data)

    return df.to_html()

### Scraping the webpage for the featured image of Mars:

def scrape_featured_image(browser):
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')

    url_list=[]

    for link in image_soup.find_all('a', class_="showimg fancybox-thumbs"):

        featured_url=link.get('href')
        featured_image_url=f'{image_url}{featured_url}'
        url_list.append(featured_image_url)

    return url_list
    
### Scraping the webpage for the Hemisphere Titles & URLs to the high resolution images:

def mars_img_links(browser):

    url = "https://marshemispheres.com/"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')

    links = soup.find_all("div", class_="item")

### Creating a list of URLs to iterate through in order to extract the image links and appending to url_list object:

    url = "https://marshemispheres.com/"
    url_list = [] 

    for link in links:
        url_list.append(f"{url}{link.find('a', class_='itemLink')['href']}")

### For loop iterating over the url_list object, extracting the Image URL & Title and storing the results in a dictionary:

    image_url_list = []

    for url in url_list:

        browser.visit(url)
        time.sleep(5)
        html = browser.html
        soup = bs(html, 'html.parser')
    
        image_url = soup.find('img', class_="wide-image")['src']
        title = soup.find('h2', class_="title").text

        image_url_list.append({"title": title,"image_url": f"https://marshemispheres.com/{image_url}"})
        
    return image_url_list


### Storing each of the results of the above webscraping into a dictionary which will be referenced when the Flask APP is rendered to generate results for the HTML page:

### Scrape all function:

def scrape_all():

    current_browser=init_browser()

    news_headline = scrape_headline(current_browser)
    news_paragraph = scrape_paragraph(current_browser)
    mars_facts = data_frame()
    featured_image = scrape_featured_image(current_browser)
    mars_image_links = mars_img_links(current_browser)

    
    mars_data =    {

        "news": news_headline,
        "paragraph": news_paragraph,
        "mars_facts": mars_facts,
        "featured_image": featured_image,
        "hemispheres": mars_image_links
    
    }

    return mars_data




