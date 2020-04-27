
#run crawl every xx hours - schedule
	#DONE - delete or create new db to fill new data
	#scrape list of top xx uploaders
	#DONE - go to page https://www.youtube.com/user/PewDiePie + 'user' + /videos
	#get top 3 videos info - uploaded xx hours/days/weeks/years
	#DONE - if they have been uploaded in xx hours/days, then scrape views 
	#DONE - save to database: user, view count, upload time, link, host_lang, and actual name on title
	#DONE -add total subs on channel and title of video. video length time
	#query database to select top views within period, giving newer videos priority
		#can query within 12 hours, 24 hours, 36 hours, 48 hours

	#check to see whether official api or webscraping is best for this

#website updates when crawl is complete
	#webpage links to top xx videos. show top 16. load more by scrolling. total 100
	#option to show 12/24/36/48 hour lists
	#option to sort by host_lang:
	#option to narrow by genre tags (that we have listed in another db)
		#kid shows, teen shows, news, comedy, politics...
		#or narrow by user ex no jake paul




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


#insert to database. add lang later. for sqlite3
#def insert_video(userName, actualName, uploadTime, viewCount, link, subCount, videoTitle):
	#context manager. don't need to commit after every insertion
	#with conn:
		#c.execute("""INSERT INTO uploadData VALUES (:userName, 
		#	:actualName, :uploadTime, :viewCount, :link, :subCount, :videoTitle)""",
		#{'userName': userName, 'actualName': actualName, 'uploadTime': uploadTime, 
		#'viewCount':viewCount, 'link':link, 'subCount':subCount, 'videoTitle':videoTitle})

#insert for postgres
def insert_video(conn, c, userName, actualName, uploadTime, viewCount, link, subCount, videoTitle):
	with conn:
		c.execute("""INSERT INTO uploadData (userName, actualName, uploadTime, 
			viewCount, link, subCount, videoTitle) VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
			(userName, actualName, uploadTime, viewCount, link, subCount, videoTitle))

#query all users 
def query_all():
		c.execute("SELECT * FROM uploadData")
		return c.fetchall()

def query_by_time():
		c.execute("SELECT * FROM uploadData ORDER BY uploadTime ASC")
		return c.fetchall()

def query_by_views():
		c.execute("SELECT * FROM uploadData ORDER BY viewCount DESC")
		return c.fetchall()

#delete entire table
def delete_table(conn, c):
	with conn:
		c.execute("DELETE FROM uploadData")



def numberFix(view):
	d = {
		'B':9,
		'M':6,
		'K':3
	}

	if view[-1] in d:
		num, magnitude = view[:-1], view[-1]
		return Decimal(num) * 10 ** d[magnitude]
	else:
		return Decimal(view)


def getUploadData():

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

	#comment out if running on file db, not memory. add lang later
	c.execute("""CREATE TABLE IF NOT EXISTS uploadData (
			userName text,
			actualName text,
			uploadTime int,
			viewCount int,
			link text,
			subCount text,
			videoTitle text
			)""")


	#import list of youtubers
	#importing spreadsheet
	df = pd.read_excel('listofyoutubers.xlsx', sheet_name='Sheet1')

	#get columns
	columns = df.columns
	columns2 = np.asarray(columns)
	#print("Column headings: ", columns2)

	#get rows. delete nan rows
	listOfYoutubers = (df['USERNAME'].dropna()).as_matrix()
	youtubeUsernames = np.asarray(listOfYoutubers)
	#print("Category Rows: ", youtubeUsernames)


	for i in range(len(youtubeUsernames)):
		print("Youtuber: ", youtubeUsernames[i])
		browser.get('https://www.youtube.com/user/' + youtubeUsernames[i] + '/videos')

		try: 
			videoPage = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'alerts')))
			#print("Video page loaded")
			sleep(2)

		except TimeoutException:
			print("Loading video page needs more time to load")
			sleep(7)

		#grabbing most recent vid date
		mostRecentVid = browser.find_element_by_xpath('//div[@id = "metadata-line"]/span[2]').text
		print("Upload Date: ",mostRecentVid)
		correctedMostRecentVid = mostRecentVid.split()
		#print(correctedMostRecentVid)
		#print(correctedMostRecentVid[0])
		#print(correctedMostRecentVid[1])

		if ((correctedMostRecentVid[1] == 'minute') or (correctedMostRecentVid[1] =='minutes') 
		or (correctedMostRecentVid[1] == 'hour') or (correctedMostRecentVid[1] == 'hours')
		or (correctedMostRecentVid[1] =='day') or (correctedMostRecentVid[1] == 'days')):
			#print("new video phase 1")

			#narrow down further by days
			if (int(correctedMostRecentVid[0]) > 2) and (correctedMostRecentVid[1] == 'days'):
				print("old video phase 2")

			else:
				print("new video phase 2")


				#recalculate so we can search by mins
				if(int(correctedMostRecentVid[0]) == 2) and (correctedMostRecentVid[1] == 'days'):
					fixedUploadTime = 48*60

				elif(int(correctedMostRecentVid[0]) == 1) and (correctedMostRecentVid[1] == 'day'):
					fixedUploadTime = 24*60

				elif(correctedMostRecentVid[1] == 'hour') or (correctedMostRecentVid[1] == 'hours'):
					fixedUploadTime = int(correctedMostRecentVid[0])*60

				else:
					fixedUploadTime = int(correctedMostRecentVid[0])




				#need to check next vid to see if that was also uploaded in time frame

				

				#grabbing views
				mostRecentViews = browser.find_element_by_xpath('//div[@id = "metadata-line"]/span[1]').text
				print("Views: ",mostRecentViews)
				correctedMostRecentViews = mostRecentViews.split()
				#print(correctedMostRecentViews)
				viewsRecent = numberFix(correctedMostRecentViews[0])
				#print(viewsRecent)

				#prepare vars for database
				userName = youtubeUsernames[i]
				#print(type(userName))

				channelTitle = browser.find_element_by_xpath('//span[@id = "channel-title"]').text
				#print(channelTitle)
				actualName = channelTitle
				#print(type(actualName))

				#tuple
				uploadTime = fixedUploadTime
				#print(uploadTime)
				#print(type(uploadTime))

				viewCount = int(viewsRecent)
				#print(type(viewCount))

				#link to video
				linkToVid = browser.find_element_by_xpath('//a[@id = "thumbnail"]')\
					.get_attribute('href')
				#print(linkToVid)
				#'https://www.youtube.com/watch?v=oRxwrYvFSN0
				#"https://www.youtube.com/embed/jvO1GDJXOgo"
				link = linkToVid.replace("watch?v=", "embed/")
				#print(type(link))

				subscribers = browser.find_element_by_xpath('//div/yt-formatted-string[@id = "subscriber-count"]').text
				subCount = subscribers
				print(subCount)

				title = browser.find_element_by_xpath('//a[@id="video-title"]')\
					.get_attribute('title')
				videoTitle = title
				print(videoTitle)

				#"host_language":"en"
				#lang will do later

				#enter to database
				insert_video(conn, c, userName, actualName, uploadTime, viewCount, link, subCount, videoTitle)









		elif ((correctedMostRecentVid[1] == 'week') or (correctedMostRecentVid[1] == 'weeks') 
		or (correctedMostRecentVid[1] == 'month') or (correctedMostRecentVid[1] == 'months')
		or (correctedMostRecentVid[1] == 'year') or (correctedMostRecentVid[1] == 'years')):
			print("old video phase 1")

		else:
			print("couldn't determine upload date")

		sleep(2)

	#query to database doesn;t work on this one
	#query1 = query_by_time()
	#print(query1)



	#query2 = query_by_views()
	#print(query2)

	#vid1 = query2[0]
	#print(vid1)

	#vid2 = query2[1]
	#print(vid2)

	#vid3 = query2[2]
	#print(vid3)

	#vid4 = query2[3]
	#print(vid4)

	#vid5 = query2[4]
	#print(vid5)



	c.close()
	conn.close()
	browser.close()


getUploadData()




