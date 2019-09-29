# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 00:21:43 2019
@author: foowailun
"""

# Required packages
from selenium import webdriver
import datetime 
import time

# Function to get prices from bursamalaysia.com
def get_bursa_announcement_urls(webdriver_path, target_url):
    
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
    
    # Identify the number of pages available
    try:
        max_page = driver.find_element_by_class_name('bm_total_page').text
    except:
        max_page = 1
        
    print(collect_timestamp + " " + "Number of pages to crawl: " + str(max_page))    
    
    # New list to store announcement urls
    announcement_urls = []
    
    # Navigate from page to page
    for page in range(int(max_page)): 
          
        current_page_url = target_url + '&page=' + str(page + 1)
        driver.get(current_page_url)
        # Allow some time for the website to load data
        time.sleep(10) 
        print(collect_timestamp + " " + "Scraping from " + current_page_url)
        announcement_table = driver.find_element_by_class_name('bm_dataTable')
        
        # Get display table
        # output = announcement_table.text.split('\n')
        
        found_links = announcement_table.find_elements_by_tag_name('a')
         
        # Get underlying href
        hrefs = []
        for link in found_links:
            link_url = link.get_attribute("href")
            
            # Append only if the href starts with this url string
            if 'http://www.bursamalaysia.com/market/listed-companies/company-announcements/' in link_url:
                hrefs.append(link_url)
            else:
                hrefs = hrefs   
        
        # Return all announcement IDs 
        announcement_urls.extend(hrefs)
        
    # Quit webdriver
    driver.quit()
    
   # Display result
    print(collect_timestamp + " " + "Gathered announcement " + str(len(announcement_urls)) + " urls.")
    time.sleep(1) 
    print(collect_timestamp + " " + "Done")
    
    #  Return announcement urls
    return(announcement_urls)

    
