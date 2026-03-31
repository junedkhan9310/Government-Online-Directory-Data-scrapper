import json
import re
import time
import sys, os
from datetime import datetime

from selenium.webdriver.common.by import By
from insert_on_database import *

from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup



urls = ["https://igod.gov.in/categories"]

def print_exception_details(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    # Extract relevant information
    Exception_Type = exc_type.__name__
    Line_No = exc_tb.tb_lineno
    Error_Message = str(e)
    if '(Session info:' in Error_Message:
        Error_Message = Error_Message.partition('(Session info:')[0].strip()
    Error_Message = Error_Message.replace('\n',', ')
    Function_name = exc_tb.tb_frame.f_code.co_name
    File_Name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    Timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Timestamp of the error occurrence
    # Construct the error message with all relevant details
    Error_Final = (
        f"Timestamp: {Timestamp} | Error_Message: {Error_Message} | "
        f"Function: {Function_name} | Exception_Type: {Exception_Type} | "
        f"File_Name: {File_Name} | Line_No: {Line_No} "
    )
    # Print the error message
    print(Error_Final)
    # Optionally, sleep to allow for error inspection (can be removed if not needed)
    time.sleep(10)



def scroll_to_bottom(driver, pause_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)  # Wait for new content to load

        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Reached the bottom
        last_height = new_height


def init_driver():
    while True:
        try:
            chrome_options = Options()
            service = Service('C:\\Translation Exe\\chromedriver.exe')  # Update with your chromedriver path
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.maximize_window()
            return driver
        except Exception as e:
            print_exception_details(e)

urls = ["https://igod.gov.in/categories"]

def Scrap():
    browser = init_driver()

    finalizedLink = []
    i = 0

    while i < len(urls):
        url = urls[i]
        print(f"Processing {url}")
        browser.get(url)
        try:
            get_htmlsource = browser.find_element(By.CLASS_NAME, "content-row").get_attribute('outerHTML')
            soup = BeautifulSoup(get_htmlsource, "html.parser")
            all_links = soup.find_all("a", href=True)

            for a in all_links:
                link = a['href']
                if "igod.gov.in" in link:
                    if link not in urls:
                        urls.append(link)
                        with open("totraverse.txt", "a", encoding="utf-8") as f:
                            f.write(link+"         ")

                else:
                    finalizedLink.append(link)
                    with open("finalized.txt", "a", encoding="utf-8") as f:
                        f.write(link+"         ")


        except Exception as e:
            print_exception_details(e)
        i += 1



Scrap()