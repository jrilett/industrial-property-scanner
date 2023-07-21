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

from abc import ABC, abstractmethod

class SiteScraper(ABC):
    
    def __init__(self, url, driver_path = '../webdriver/geckodriver'):
        self.url = url
        self.driver_path = driver_path

    @abstractmethod
    def access_site(self):
        pass
    
    @abstractmethod
    def scrape_site(self):
        pass
    
