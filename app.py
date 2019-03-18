#!/usr/bin/env python

import os
import getpass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser
config = configparser.ConfigParser()
config.read('config.ini')


if os.path.exists('config.ini'):
	username = config['default']['user']
	password = config['default']['passwd']
else:
	#prompt for credentials
	username = input("Please enter your username: ")
	password = getpass.getpass('Password:')

chrome_driver_path = "/usr/local/bin/chromedriver"
#build chrome oprions
chrome_options = Options()
#chrome_options.add_argument("--headless")#run in headless mode
driver = webdriver.Chrome(executable_path=os.path.abspath(chrome_driver_path),
                          options=chrome_options)

driver.get("https://my.chevrolet.com/electric-vehicle")

user = driver.find_element_by_id("login_username")
passwd = driver.find_element_by_id("login_password")
#enter username & password
user.send_keys(username)
passwd.send_keys(password)
#send return
passwd.send_keys(u'\ue007')

#timeout is set to 3 mins(from chevy site)
timeout = 120
try:
	element_charging_status_css_path = '#content > div > div > div.container > div.row > div > div > div.evHomeStatus.ng-scope.ng-isolate-scope > div > div.ev-status-container.ng-scope > div.ev-status-left > div.ev-battery-margin > span'
	element_css_path = '#content > div > div > div.container > div.row > div > div > div.evHomeStatus.ng-scope.ng-isolate-scope > div > div.ev-status-container.ng-scope > div.ev-status-left > h1'
	element_miles_css_path = '#content > div > div > div.container > div.row > div > div > div.evHomeStatus.ng-scope.ng-isolate-scope > div > div.ev-status-container.ng-scope > div.ev-miles-container > div.ev-miles-height > div > div:nth-child(1) > h1'
	element_charge_completion_time_css_path = '#content > div > div > div.container > div.row > div > div > div.evHomeStatus.ng-scope.ng-isolate-scope > div > div.ev-status-container.ng-scope > div.ev-status-left > div.ev-charge-state > div'
	element_present = EC.visibility_of_element_located((By.CSS_SELECTOR, element_css_path))
	print('**Thanks for waiting! It may take three minutes to retrieve your data.**')
	WebDriverWait(driver, timeout).until(element_present)
	print('Current Status : ' + driver.find_elements_by_css_selector(element_charging_status_css_path)[0].text)
	print('Battery level : ' + driver.find_elements_by_css_selector(element_css_path)[0].text)
	print('Estimated Range : ' + driver.find_elements_by_css_selector(element_miles_css_path)[0].text + " Electric Miles")
	print(driver.find_elements_by_css_selector(element_charge_completion_time_css_path)[0].text)
except TimeoutException:
    print("Timed out waiting for page to load")