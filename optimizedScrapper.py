import os
import sys
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

# Custom import
from insert_on_database import *


# --- Utility to print detailed exceptions ---
def print_exception_details(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    Exception_Type = exc_type.__name__
    Line_No = exc_tb.tb_lineno
    Error_Message = str(e).partition('(Session info:')[0].strip().replace('\n', ', ')
    Function_name = exc_tb.tb_frame.f_code.co_name
    File_Name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    Timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    Error_Final = (
        f"Timestamp: {Timestamp} | Error_Message: {Error_Message} | "
        f"Function: {Function_name} | Exception_Type: {Exception_Type} | "
        f"File_Name: {File_Name} | Line_No: {Line_No}"
    )
    print(Error_Final)

def scroll_to_bottom(driver, pause_time=2, max_attempts=10):
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempts = 0
    while attempts < max_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            attempts += 1  # No change in height
        else:
            attempts = 0  # Reset if new content appeared
        last_height = new_height

def load_set_from_file(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_set_to_file(filename, data_set):
    with open(filename, "w", encoding="utf-8") as f:
        for item in data_set:
            f.write(item + "\n")


# --- Initialize WebDriver ---
def init_driver():
    while True:
        try:
            chrome_options = Options()
            service = Service('C:\\Translation Exe\\chromedriver.exe')  # Path to chromedriver
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.maximize_window()
            return driver
        except Exception as e:
            print_exception_details(e)
            time.sleep(5)  # Retry delay


# --- Main Scraping Function ---
def scrap():
    browser = init_driver()

    # Load previous state
    visited_urls = load_set_from_file("visited.txt")
    to_traverse = load_set_from_file("to_traverse.txt")
    if not to_traverse:
        to_traverse = {"https://igod.gov.in/categories"}  # Starting point if fresh run

    finalized_links = load_set_from_file("finalized.txt")
    duplicatelink = 0

    # visited_urls = set()
    # to_traverse = set(["https://igod.gov.in/categories"])
    # finalized_links = set()
    # duplicatelink = 0
    try:
        while to_traverse:
            url = to_traverse.pop()
            print(f"Processing: {url}")
            visited_urls.add(url)
            save_set_to_file("visited.txt", visited_urls)
            save_set_to_file("to_traverse.txt", to_traverse)
            save_set_to_file("finalized.txt", finalized_links)

            try:
                browser.get(url)
                scroll_to_bottom(browser)  # Scroll until the page stops growing
                element = browser.find_element(By.CLASS_NAME, "content-row")
                content = element.get_attribute('outerHTML')
                # content = browser.find_element(By.CSS_SELECTOR, "div.col-lg-8.col-md-12.col-sm-12").get_attribute('outerHTML')

                soup = BeautifulSoup(content, "html.parser")


                for div in soup.find_all("div", class_="col-lg-4 col-md-12 col-sm-12"):
                    if div.find("aside"):
                        div.decompose()

                all_links = soup.find_all("a", href=True)

                for tag in all_links:
                    link = tag['href']
                    if any(link.startswith(prefix) for prefix in ["tel:", "mailto:", "javascript:", "#"]):
                        continue

                    if link == "https://lgdirectory.gov.in":
                        continue

                    if "igod.gov.in" in link:
                        if link not in visited_urls and link not in to_traverse:
                            to_traverse.add(link)
                    else:
                        if link not in finalized_links:
                            insert_on_table(link)
                            finalized_links.add(link)
                        else:
                            duplicatelink+=1
                            print("the count of duplication happening is ",link)

            except NoSuchElementException:
                continue  # Element not found, just skip this page
            except Exception as e:
                print_exception_details(e)

    finally:
        browser.quit()  # Ensure browser closes on exit

        # Write collected links to files
        try:
            with open("totraverse.txt", "w", encoding="utf-8") as f:
                for link in visited_urls:
                    f.write(link + "\n")
            with open("finalized.txt", "w", encoding="utf-8") as f:
                for link in finalized_links:
                    f.write(link + "\n")
        except Exception as file_error:
            print_exception_details(file_error)


# --- Run the scraper ---
if __name__ == "__main__":
    scrap()
