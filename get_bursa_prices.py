# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 00:21:43 2019
@author: foowailun
"""

# Required packages
from selenium import webdriver
import datetime 
import time
import pandas as pd

# Function to get prices from bursamalaysia.com
def get_bursa_prices(webdriver_path, target_url):

    # Set up webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(webdriver_path, chrome_options=chrome_options)
    
    # Set collection time to malaysian time i.e. UTC + 8
    malaysia_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours = 8)
    collect_timestamp = malaysia_datetime.strftime('%Y-%m-%d_%H-%M-%S')
    
    # Collect data from target url
    driver.get(target_url)
    print(collect_timestamp + " " + "Collecting data from " + target_url)
    # Allow some time for the website to load data
    time.sleep(10) 
    price_table = driver.find_element_by_id('bm_price_container')
    output = price_table.text.split('\n')
    
    # Quit webdriver
    driver.quit()
    
    # Clean and transform data
    price_list = []
    for word in output:
        # Remove the spacing for ' [S]' and remove ',' in numeric values
        word = word.replace(" [S]","[S]").replace(",","").split(" ")
        price_list.append(word)
    
    # Set up data frame
    table_names = pd.DataFrame(price_list[0])
    table_body = pd.DataFrame(price_list[1:])
    price_table = table_body.rename(columns = table_names[0])
    
    # Add new column to indicate date time
    price_table.insert(loc = 0, column = "Collect_DateTime", value = collect_timestamp)
    
    # Display result
    print(collect_timestamp + " " + "Gathered prices from" + " " + str(len(price_table)) + " " + "stocks.")
    time.sleep(1) 
    print(collect_timestamp + " " + "Done")
    
    # Return prices
    return(price_table)
    
    
