# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import time
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
    
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')
    #scraping site to find latest title and assigning it to a variable
    titles = soup.find('div', class_='content_title')
    news_title = titles.text  

    #scraping site to find latest paragraph and assigning it to a variable
    html = browser.html
    soup = bs(html, 'html.parser')
    #scraping site to find latest paragraph and assigning it to a variable
    paragraphs = soup.find('div', class_='article_teaser_body')
    news_p = paragraphs.text  

    # using splinter to navigate and find the image url for the current Featured Mars Image 
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')
    #assigning image url to 'featured_image_url' variable
    image = soup.find('a', target ='_blank' )['href']
    featured_image_url = f'{image_url}{image}'

    # using pandas 'read html' to pars the url
    tables_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(tables_url)
    html_tables = tables[0]
    # reset columns and index for cleaner table
    html_tables.columns = ["","Mars","Earth"]
    html_tables.set_index("", inplace=True)

    #Use Pandas to convert the data to a HTML table string
    mars_facts = html_tables.to_html()
   

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


    # created list of dictionary from title and image url list and named hemisphere_image_urls list
    hemisphere_image_urls = []
    for i in range(len(title)):
        hemisphere_image_urls.append({'title':title[i],'img_url':f"https://marshemispheres.com/{image_url[i]}"})

    #Mars Dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image_URL": featured_image_url,
        "html_table": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls 
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data






