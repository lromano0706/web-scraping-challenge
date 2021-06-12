# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    #Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


     # URL of page to be scraped
    url = "https://redplanetscience.com/"
    browser.visit(url)


    #scraping site to find latest title and assigning it to a variable
    html = browser.html
    soup = bs(html, 'html.parser')
    titles = soup.find('div', class_='content_title')
    news_title = titles.text  
    news_title


    #scraping site to find latest paragraph and assigning it to a variable
    html = browser.html
    soup = bs(html, 'html.parser')
    paragraphs = soup.find('div', class_='article_teaser_body')
    news_p = paragraphs.text  
    news_p

    # using splinter to navigate and find the image url for the current Featured Mars Image 

    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)


    #assigning image url to 'featured_image_url' variable
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find('a', target ='_blank' )['href']
    featured_image_url = f'{image_url}{image}'
    featured_image_url


    # using pandas 'read html' to pars the url
    tables_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(tables_url)
    html_tables = tables[0]
    html_tables



    #Use Pandas to convert the data to a HTML table string
    mars_facts = html_tables.to_html()
    mars_facts



    #Mars Hemispheres scrape and for loop to put tile and url in a list
    Mars_image_url = 'https://marshemispheres.com/'
    browser.visit(Mars_image_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    images = soup.find_all('h3')
    title = []
    image_url = []
    for image in images[:4]:
        browser.links.find_by_partial_text(image.text).click()
        title.append(image.text)
        html = browser.html
        soup = bs(html, 'html.parser')
        url = soup.find('img', class_="wide-image")['src']
        image_url.append(url)
        browser.links.find_by_partial_text('Back').click()



    # created dictionary from tile and image url list and converted them into a hemisphere_image_urls list
    hemisphere_image_urls = []
    for i in range(len(title)):
        hemisphere_image_urls.append({'title':title[i],'img_url':f"https://marshemispheres.com/{image_url[i]}"})







