import os
import sys
import pip._vendor.requests as requests
import bs4
from bs4 import BeautifulSoup
import re
import warnings
import time
import codecs
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument("--log-level=3")
options.add_argument("--window-size=1920,1080")

chrome_driver = r"C:/users/arivappa/documents/seleniumDrivers/chromedriver_108.exe"
ser = Service(chrome_driver)
driver = webdriver.Chrome(service=ser, options=options)
# driver = webdriver.Chrome(executable_path=chrome_driver, options=options)

def clean_data(input):
    input = input.lower()
    input = input.replace("\n", " ").replace("\t", " ").strip()
    return input

def get_quotes(url):
    driver.get(url)
    innerHTML = driver.page_source
    soup = BeautifulSoup(innerHTML, 'html.parser')

    main_div = soup.find('div', attrs={'class': 'quotes'})

    # ## remove image divs
    # for img_comp in main_div.select('div', attrs={'class': 'qti-listm'}):
    #     img_comp.extract()

    curr_file = open('./quotes.txt', 'a', encoding='utf-8')

    for quote_div in main_div.find_all('div', attrs={'class': 'quote'}):
        text_div = quote_div.find('div', attrs={'class': 'quoteText'})
        text = clean_data(text_div.text)
        curr_file.write(text)
        curr_file.write("\n")

    curr_file.close()

pre_link = "https://www.goodreads.com/quotes"
pages_count = 15

for page_no in range(1, pages_count):
    if page_no > 1:
        link = pre_link + "?page=" + str(page_no)
    else:
        link = pre_link
    try:
        get_quotes(link)
        print("Completed " + link[link.rfind('/')+1:])
    except Exception:
        notfound_file = open('notfound.txt', 'a', encoding='utf-8')
        notfound_file.write(link)
        notfound_file.write("\n")
        notfound_file.close()
        print("Exception in " + link)

driver.close()
