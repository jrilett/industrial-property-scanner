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
from src.python.SiteScraper import SiteScraper

class AvisonYoungScraper(SiteScraper):

    def scrape_site(self):
        for parent_page in self.url_list:

            self.driver.get(parent_page)
            
            self._cookie_click()
            self.scrape_parent_page(parent_page)
        
        for p_url, parent_url in self.property_url_list:
            self.scrape_individual_site_page(p_url, parent_url)

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
