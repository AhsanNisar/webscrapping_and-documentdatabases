'''This program is written to extract the mars information including
the images and the fact sheet for mars
Created By: Muhammad Ahsan for 
Data Analytics and Visuaization boot camp'''

# Importing the required packages 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import os 
import time
# function to start the browser
def Browser():
    #starting the chrome browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


#Scraping the mars information
def mars_function():
    try:
        browser = Browser()
       
        #Initializing an empty dictionary to store all mars data
        mars_data ={}
        
        #NASA mars News Site
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)
        # storing the content in a variable
        html = browser.html
        # parse the elements of html using beautiful soup
        soup = bs(html, 'html.parser')




        # collect the latest News Title and Paragraph Text
        title = soup.find("div", class_="content_title").text
        paragraph = soup.find("div", class_="article_teaser_body").text
        


        # use splinter functions https://splinter.readthedocs.io/en/latest/api/driver-and-element-api.html
        base_url = 'https://www.jpl.nasa.gov'
        mars_url = base_url + '/spaceimages/?search=&category=Mars'
        browser.visit(mars_url)
        browser.is_text_present('Full IMAGE')
        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(2)

        image_html = browser.html
        image_bs = bs(image_html, 'html.parser')

        image_url = image_bs.find('div', class_='fancybox-inner').img['src']


        featured_image_url = base_url + image_url



        # scrape mars weather info from official twitter account page
        mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(mars_weather_url)
        time.sleep(2)

        mars_weather_html = browser.html

        mars_weather_bs = bs(mars_weather_html, 'lxml')

        # split the text to retrieve relevant info
        mars_weather = mars_weather_bs.find('p', class_='tweet-text').text.split("pic")[0]


        # URL for mars facts table
        mars_facts_url = 'https://space-facts.com/mars/'

        mars_facts_table = pd.read_html(mars_facts_url)
        time.sleep(2)
        df = mars_facts_table[0]
        df.columns = ['Names', 'Value']

        # convert data frame to html
        mars_factsheet = df.to_html(index=False, justify ='center')

        # writing dataframe to html file - it would be nice to flatten column head into same row though
        with open('mars_facts.html', 'w') as mars:
            df.to_html(mars)


        hemisphere_base_url = 'https://astrogeology.usgs.gov'
        hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=mars'
        browser.visit(hemisphere_url)
        time.sleep(5)

        hemisphere_html = browser.html
        hemisphere_bs = bs(hemisphere_html, 'html.parser')
        items = hemisphere_bs.find_all('div', class_="item")
        hemisphere_image_dict = []


        for item in items:
            title = item.find('h3').text
            image_url = item.find('a', class_='itemLink product-item')['href']
            browser.visit(hemisphere_base_url + image_url)
            image_html = browser.html
            soup = bs(image_html, 'html.parser')
            image_url = hemisphere_base_url + soup.find('img', class_='wide-image')['src']
            hemisphere_image_dict.append(
                {
                    "title":title,
                    "image_url": image_url
                }
            )

        hemisphere_image_dict


        mars_data['title'] = title
        mars_data['paragraph'] = paragraph
        mars_data["featured_image_url"] = featured_image_url
        mars_data['mars_weather'] = mars_weather
        mars_data['mars_facts'] = mars_factsheet
        mars_data["hemisphere_dict"] = hemisphere_image_dict
        return mars_data


    finally:
        browser.quit()
        
        
# debugging using the following lines
if __name__ == "__main__":
    listings = scrape()
    print(listings)