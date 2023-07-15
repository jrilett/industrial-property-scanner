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

# Specify the path to geckodriver
driver_path = '../webdriver/geckodriver'

service = Service(driver_path)
driver = webdriver.Firefox(service=service)


# input URL - we should have a list to iterate through but the sites may have different layouts from one another
url = ''

# driver opens the browers on yr pc 
driver.get(url)

# this scrolls to the bottom of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# find an element called load more and mouse click it
driver.find_element_by_link_text("Load More").click()

# grab the static page now
soup = BeautifulSoup(driver.page_source, 'lxml')

# need to iterate through the page items to get the info

# example of find all list items on the page with the class name
#soup.find_all('li', class_="quote-news-headlines__item")[0].find('a')['href']