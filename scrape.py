



import os

#import sqlite3

import psycopg2

import pandas as pd
import requests
import time
from time import sleep
import numpy as np
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from decimal import Decimal

#headless chromedriver config to run on local server
#options = Options()
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')

#headless chromedriver config to run on cloud server
#chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
#chrome_options = Options()
#chrome_options.binary_location = chrome_bin
#chrome_options.add_argument('--disable-gpu')
#chrome_options.add_argument('--no-sandbox')


#start session in chrome on local server
#if want to use headless
#browser = webdriver.Chrome('./assets/chromedriver', chrome_options=options)
#if want to see chrome
browser = webdriver.Chrome('./assets/chromedriver')

#start session in chrome on CLOUD SERVER
#browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)


#starting database with sqlite3
#two options to store:
##1 - in memory - lives in ram. good for testing. starts from scratch
#conn = sqlite3.connect(':memory:')
##2 - in file. creates file or connects to it
#conn = sqlite3.connect('burstDB.db')

#starting db with postgres on local comp
conn = psycopg2.connect(host="localhost", database="youtubedb", user="", password="")

#executes sql commands on both sqlite3 and postgres
c = conn.cursor()
print("connected to db")

c.execute("CREATE TABLE IF NOT EXISTS scrapeData (userName text)")



#insert for postgres
def insertusername(youtuberFixed1):
	with conn:
		c.execute("INSERT INTO scrapeData (userName) VALUES (%s)", (youtuberFixed1,))






def scrape():
	link = 'https://www.listubes.com/top2000/'
	webPages = [link, link+'?p=2', link+'?p=3', link+'?p=4', link+'?p=5', link+'?p=6', 
	link+'?p=7', link+'?p=8', link+'?p=9', link+'?p=10', link+'?p=11', link+'?p=12',
	link+'?p=13', link+'?p=14', link+'?p=15', link+'?p=16', link+'?p=17', link+'?p=18',
	link+'?p=19', link+'?p=20']

	n = 0

	for i in range(len(webPages)):
		

	

		browser.get(webPages[n])
		#?p=2 ?p=3 up to 20

		try: 
			videoPage = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'i1')))
			#print("Video page loaded")
			sleep(2)

		except TimeoutException:
			print("Loading video page needs more time to load")
			sleep(7)

		sleep(2)


		loop = 0
		loop1 = 0
		nextUser = True
		nextUser1 = True

		while nextUser == True:


			try:
				youtuber = browser.find_elements_by_xpath('//tr[@class = "un"]/td/div/a')[loop]\
					.get_attribute('href')

				youtuberFixed = youtuber.replace("https://www.listubes.com/user/", "")

				youtuberFixed1 = youtuberFixed.replace("https://www.listubes.com/", "")

				insertusername(youtuberFixed1)

				#print("inserted user")

				loop += 1

			except NoSuchElementException:
				nextUser = False

			except IndexError:
				nextUser = False

		while nextUser1 == True:

			try:
				youtuber = browser.find_elements_by_xpath('//tr[@class = "two"]/td/div/a')[loop1]\
					.get_attribute('href')

				youtuberFixed = youtuber.replace("https://www.listubes.com/user/", "")

				youtuberFixed1 = youtuberFixed.replace("https://www.listubes.com/", "")

				#youtuberFixed1 = youtuberFixed.replace("/", "")

				insertusername(youtuberFixed1)

				print("inserted user")



				loop1 += 1

			except NoSuchElementException:
				nextUser1 = False

			except IndexError:
				nextUser1 = False

		print("loop complete")

		n += 1
		sleep(2)






		
scrape()


c.close()
conn.close()
browser.close()






