import pandas as pd
import numpy as np
import re
import requests
import warnings

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys
from random import randint
import pandas as pd
import time
import re


class job_search:
    
    def __init__(self, title, location, n_pages):
        
        self.title = title
        self.location = location
        self.n_pages = n_pages
        
        warnings.filterwarnings("ignore")
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox") 
        
        driver = webdriver.Chrome(chrome_options = options)
        driver.set_page_load_timeout(25)
        self.driver = driver
        
        self.url = "https://sg.indeed.com/"
        self.driver.get(self.url)
                
        job_search_bar = self.driver.find_element(By.ID, "text-input-what")
        job_search_bar.send_keys(title)
        time.sleep(randint(2, 5))

        location_search_bar = self.driver.find_element(By.ID, "text-input-where")
        location_search_bar.send_keys(location)
        time.sleep(randint(2, 5))

        # submit the search
        self.driver.find_element(By.XPATH, '//button[@class="yosegi-InlineWhatWhere-primaryButton"]').click()
        time.sleep(randint(2, 5))
        
        self.results = pd.DataFrame({"job_title": [], "company": [], "job_ad": []})
        
        
        
    def webscrape(self):
        """
        function for retrieving the relevant information on the search page
        """
        
        results = self.driver.find_elements(By.XPATH, '//*[@class="resultContent"]')

        for result in results:
            # collect job title and company (if any)
            html = result.get_attribute('innerHTML')
            data = BeautifulSoup(html, 'html.parser')
            url_extension = data.a.attrs['href']
            entry = ["", "", ""]
            
            for index, row in enumerate(data.findAll("a")[:2]):
                entry[index] = row.get_text()
                
            # add url
            entry[-1] = self.url + url_extension
            
            entry_df = pd.DataFrame.from_records(data=[entry], columns=self.results.columns)            
            self.results = pd.concat([self.results, entry_df], ignore_index=True)
            
    
    def parse_n_pages(self, n_pages=10):
        """
        function that specifies the number of pages to scrape
        """
        
        job_title_for_search = self.title.split(" ")
        job_title_for_search = "+".join(job_title_for_search)
        
        location_for_search = self.location.split(" ")
        location_for_search = "+".join(location_for_search)
            
        for i in range(1, 1+n_pages):
            
            self.webscrape()
            time.sleep(randint(2, 5))
            
            navigate_next = 'https://sg.indeed.com/jobs?q={}&l={}&start={}'.format(job_title_for_search, \
                                                                                   location_for_search, i*10)
            
            self.driver.get(navigate_next)
            time.sleep(randint(2,5))
            
        print("---Webscraping completed---")
        
        
    def main(self):
        """
        main function to run
        """
        
        return self.parse_n_pages(n_pages=self.n_pages) 
        
        
