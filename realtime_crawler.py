# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 16:15:54 2019
@author: foowailun
"""

# Requred packages
import datetime
import time
import schedule

# Required modules
from get_bursa_prices import get_bursa_prices
from get_bursa_announcement_urls import get_bursa_announcement_urls
from get_bursa_announcement_details import get_bursa_announcement_details

# Set parameters
webdriver_PATH = "usr/local/bin/chromedriver" 

# Wrapper function
def run_crawler():
    # Today's date
    current_date = datetime.datetime.utcnow() + datetime.timedelta(hours = 8)
    
    # Get price data 
    price_data = get_bursa_prices(webdriver_PATH, 'http://www.bursamalaysia.com/market/securities/equities/prices/#/?filter=BS08&board=MAIN-MKT&page=1')
    
    # Output to txt to store
    price_data.to_csv(current_date.strftime('%Y-%m-%d') + "_" + "price_table" +  ".csv")
    
    # Get announcement data                  
    announcement_urls = get_bursa_announcement_urls(webdriver_PATH, 'http://www.bursamalaysia.com/market/listed-companies/company-announcements/#/?category=SH&sub_category=SH3&alphabetical=All&date_from=' + current_date.strftime('%d/%m/%Y') + '&date_to=' + current_date.strftime('%d/%m/%Y') + '&board=MAIN-MKT')
                                                    
    for announcement_url in announcement_urls:  
       # Get announcement data 
       full_announcement_data = get_bursa_announcement_details(webdriver_PATH, announcement_url)
       # Output to txt to store
       outFile = open("announcements.txt", "a")
       print(current_date.strftime('%Y-%m-%d_%H-%M-%S') + " " + "Writing txt files for " + announcement_url)
       outFile.writelines(full_announcement_data)
       outFile.close()

# Schedule task at 11pm daily
schedule.every().day.at("23:00").do(run_crawler)

# Loop infinitely
while True:
    schedule.run_pending()
    time.sleep(1)


