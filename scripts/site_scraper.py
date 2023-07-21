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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
from abc import ABC, abstractmethod
from src.python.AvisionSiteScraper import AvisonYoungScraper

a_v_y_scraper = AvisonYoungScraper(["https://www.avisonyoung.co.uk/properties/-/property/results?industrial=1&south_west=1&units=sqft&size_min_sqft=-1&size_min_sqm=-1&size_min_acres=-1&size_max_sqft=0&size_max_sqm=0&size_max_acres=0&submit=SEARCH&type=r"])
                    #"https://www.avisonyoung.co.uk/properties/-/property/results?office=1&flex-office=1&retail=1&south_west=1&units=sqft&size_min_sqft=-1&size_min_sqm=-1&size_min_acres=-1&size_max_sqft=0&size_max_sqm=0&size_max_acres=0&submit=SEARCH&type=r"])

a_v_y_scraper.scrape_site()

pd.DataFrame(a_v_y_scraper.property_info).to_csv('class_Test.csv')

'''
# this scrolls to the bottom of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# find an element called load more and mouse click it
driver.find_element_by_link_text("Load More").click()

# grab the static page now
soup = BeautifulSoup(driver.page_source, 'lxml')

# need to iterate through the page items to get the info

# example of find all list items on the page with the class name
soup.find_all('li', class_="quote-news-headlines__item")[0].find('a')['href']

'''
