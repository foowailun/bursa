# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 00:21:43 2019
@author: foowailun
"""

# Required packages
from selenium import webdriver
import datetime 
import time
import json

# Function to get prices from bursamalaysia.com
def get_bursa_announcement_details(webdriver_path, target_url):
    
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
    print(collect_timestamp + " " + "Navigating to " + target_url)
    # Allow some time for the website to load data
    time.sleep(2) 
    # Get the alternative page that renders data in html
    target_alt_url = driver.find_element_by_id('bm_ann_detail_iframe').get_attribute("src")
    
    # Collect data from target url   
    print(collect_timestamp + " " + "Scraping from " + target_alt_url)
    driver.get(target_alt_url)
    # Allow some time for the website to load data
    time.sleep(2) 
    
    # Extract useful elements 
    a = driver.find_elements_by_class_name('InputTable2')[0].text.split('\n')
    b = driver.find_elements_by_class_name('InputTable2')[1].text.split('\n') 
    c = driver.find_element_by_class_name('ven_announcement_info').text.split('\n')
    d = driver.find_element_by_class_name('ven_table').text.split('\n')

    # Compile data
    text_dump = {"Source" : target_alt_url,
         "Date Announced" : c[3].replace("Date Announced",""),
         "Category " : c[4].replace("Category",""),
         "Stock Name" : c[2].replace("Stock Name",""),
         "Company Name" : c[1].replace("Company Name",""),
         "Shareholder Name" : a[0].replace("Name","") ,
         "Class" : a[-1].replace("Descriptions (Class)",""),
         "Indirect/deemed interest (%)" : b[-4].replace("Indirect/deemed interest (%)",""), 
         "Indirect/deemed interest (units)" : b[-5].replace("Indirect/deemed interest (units)",""),
         "Direct (%)" : b[-6].replace("Direct (%)",""),
         "Direct (units) 1,463,774,894" : b[-7].replace("Direct (units)",""),
         "Post No. of Securities" : b[-3].replace("Total no of securities after change",""), 
         "Detailed Transaction" : d[4:]}
    
    output = json.dumps(text_dump)
    
    # Quit webdrier
    driver.quit()
    
    # Display result
    print(collect_timestamp + " " + "Done")
    
    #  Return announcement urls
    return(output)
