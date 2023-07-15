import requests
import os
from bs4 import BeautifulSoup 
import csv
import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.firefox import DriverManager
from time import time, sleep
from selenium.webdriver.firefox.service import Service
import pickle

# Specify the path to geckodriver
driver_path = '../webdriver/geckodriver'

service = Service(driver_path)
driver = webdriver.Firefox(service=service)


# input URL - we should have a list to iterate through but the sites may have different layouts from one another
url = "https://www.avisonyoung.co.uk/properties/-/property/results?south_west=1&units=sqft&size_min_sqft=-1&size_min_sqm=-1&size_min_acres=-1&size_max_sqft=0&size_max_sqm=0&size_max_acres=0&address=&submit=Search+Properties&type=r"
cookies = pickle.load(open("scripts/cookies.pkl", "rb"))
driver.get(url)
for cookie in cookies:
    driver.add_cookie(cookie)
# driver opens the browers on yr pc 


soup = BeautifulSoup(driver.page_source, 'html')
grid_item = soup.find_all("section", class_='grid-item')

property_url_list = [x.find('a')["href"] for x in grid_item]
property_info = []
for p_url in property_url_list : 
    driver.get(p_url)
    property_soup = BeautifulSoup(driver.page_source, 'html')
    
    try:
        property_cost = property_soup.find_all("div", class_ = "right")[1].find("pre").text
    except:
        property_cost = ''   
    try:
        property_size_sqft = property_soup.find("p", class_ = "sqft").text
    except:
        property_size_sqft = ''
    try:
        property_size_sqm = property_soup.find("p", class_ = "sqm").text
    except:
        property_size_sqm = ''
    try:    
        property_address = property_soup.find("div", class_ = "top").text
    except:
        property_address = ''
    try:
        property_epc = property_soup.find("div", class_ = "epc").text
    except:
        property_epc = ''


    property_info.append([p_url, property_address, property_cost, property_size_sqft, property_size_sqm, property_epc])
    sleep(5)
    print(p_url)

pd.DataFrame(property_info, columns = ['url','address', 'cost', 'size_sqft', 'size_sqm','epc']).to_csv("first_db.csv")





# this scrolls to the bottom of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# find an element called load more and mouse click it
driver.find_element_by_link_text("Load More").click()

# grab the static page now
soup = BeautifulSoup(driver.page_source, 'lxml')

# need to iterate through the page items to get the info

# example of find all list items on the page with the class name
#soup.find_all('li', class_="quote-news-headlines__item")[0].find('a')['href']