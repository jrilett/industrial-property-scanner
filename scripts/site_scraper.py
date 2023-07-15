import requests
from bs4 import BeautifulSoup 
import csv
import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.firefox import DriverManager
from time import time, sleep

# need to check if i am running or if james is as he is using edge
driver = webdriver.Firefox(executable_path='./geckodriver')

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