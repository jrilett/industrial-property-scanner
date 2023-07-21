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

class SiteScraper(ABC):

    def __init__(self, url_list, driver_path = '../webdriver/geckodriver'):
        self.url_list = url_list
        self.property_url_list = []
        self.property_info = []
        # start up selenium assign driver to self
        service = Service(driver_path)
        self.driver = webdriver.Firefox(service=service)

        self.scrape_site()
        self.return_data()

    @abstractmethod
    def scrape_site(self):
        pass

    @abstractmethod
    def scrape_individual_site_page(self):
        pass
    
    @abstractmethod
    def _cookie_click(self):
        pass
    
    @abstractmethod
    def scrape_parent_page(self):
        pass

    @abstractmethod
    def return_data(self):
        pass

class AvisonYoungScraper(SiteScraper):

    def scrape_site(self):
        for parent_page in self.url_list:

            self.driver.get(parent_page)
            
            self._cookie_click()
            self.scrape_parent_page(parent_page)
        
        for p_url, parent_url in self.property_url_list:
            self.scrape_individual_site_page(p_url, parent_url)

    def _cookie_click(self):
        """
        author: lovely james
        """
        try:
            self.driver.find_element(By.ID, 'hs-eu-confirmation-button').click()
        except:
            pass

    def scrape_parent_page(self, parent_page):
        """
        TODO: add page number
        
        Scrape parent page for all available property listings

        args:
            parent_page: str - parent page of site, ie industrial or other
        """
        soup = BeautifulSoup(self.driver.page_source, 'html')
        
        grid_item = soup.find_all("section", class_='grid-item')

        self.property_url_list.extend([(x.find('a')["href"], parent_page) for x in grid_item])
        
        # get number of pages in future to scrap all available listings
        
    def scrape_individual_site_page(self, url, current_parent_page):

        self.driver.get(url)
        
        property_soup = BeautifulSoup(self.driver.page_source, 'html')

        property_type = 1 if 'industrial' in current_parent_page.lower() else 0

        ########################
        # Scrape Property Cost #
        ########################
        try:
            property_cost = property_soup.find_all("div", class_ = "right")[1].find("pre").text
        except:
            property_cost = ''

        ########################
        #   Scrape Size Sqft   #
        ########################
        try:
            property_size_sqft = property_soup.find("p", class_ = "sqft").text
        except:
            property_size_sqft = ''

        ########################
        #   Scrape Size Sqm    #
        ########################
        try:
            property_size_sqm = property_soup.find("p", class_ = "sqm").text
        except:
            property_size_sqm = ''

        ########################
        #    Scrape Address    #
        ########################
        try:    
            property_address = property_soup.find("div", class_ = "top").text
        except:
            property_address = ''

        ########################
        #  Scrape Agent Number #
        ########################
        try:
            agent_number = property_soup.find("section", class_ = "agent-details").text
        except:
            agent_number = ''

        self.property_info.append([url, property_type, property_address, property_cost, property_size_sqft, property_size_sqm, agent_number])

    def return_data(self):
        pd.DataFrame(self.property_info, columns = ['url', 'property_type', 'address', 'cost', 'size_sqft', 'size_sqm','agent_number']).to_csv("first_db.csv")


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
