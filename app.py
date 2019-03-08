#!/usr/bin/env python

import configparser
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

config = configparser.ConfigParser()
config.read("config.ini")

chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=os.path.abspath("/usr/local/bin/chromedriver"),
                          chrome_options=chrome_options)

driver.get("https://my.chevrolet.com/electric-vehicle")

user = driver.find_element_by_id("login_username")
passwd = driver.find_element_by_id("login_password")
user.send_keys(config["default"]["user"])
passwd.send_keys(config["default"]["passwd"])
passwd.send_keys(u'\ue007')
#driver.find_element_by_id("login_password").click()

timeout = 120
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'status-box'))
    WebDriverWait(driver, timeout).until(element_present)
    print(driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div[2]/div[2]/div/div/div[1]/div/div[3]/div[1]/h1').text)
    print(driver.find_element_by_class_name("status-box").text)
    print(driver.find_element_by_class_name("status-right").text)
except TimeoutException:
    print("Timed out waiting for page to load")

print("Done!")