
#run crawl every xx hours - schedule
	#DONE - delete or create new db to fill new data
	#DONE - top 2000 scrape list of top xx uploaders
	#DONE - go to page https://www.youtube.com/user/PewDiePie + 'user' + /videos
	#DONE - get most recent videos info - uploaded xx hours/days/weeks/years
	#DONE - if they have been uploaded in xx hours/days, then scrape: 
		#DONE - save to database: user, view count, upload time, link, actual name, title, sub count, etc
		#DONE - host country 
		#video length?
		#watch out for live streaming
		#watch out for reminders

	#exceptions on youtube red accts where cant find view count
	#DONE - error for channel w no username. ex: channel/UC295-Dw_tDNtZXFeAPAW6Aw/ and do not have a user/

	#maybe add in minimum views so database isn't too large



#website updates when crawl is complete
	#DONE - query database to select top views within period, giving newer videos priority
		#DONE - can query within 6 hours, 12 hours, 24 hours, 48 hours
	#webpage links to top xx videos. show top 16. load more by scrolling. total 100
		#use api to get current view count or something dynamic
	#DONE - option to show 6/12/24/36/48 hour lists
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



#insert for sqlite3
#def insert_video(userName, actualName, uploadTime, viewCount, link, subCount, videoTitle):
	#context manager. don't need to commit after every insertion
	#with conn:
		#c.execute("""INSERT INTO uploadData VALUES (:userName, 
		#	:actualName, :uploadTime, :viewCount, :link, :subCount, :videoTitle)""",
		#{'userName': userName, 'actualName': actualName, 'uploadTime': uploadTime, 
		#'viewCount':viewCount, 'link':link, 'subCount':subCount, 'videoTitle':videoTitle})

#insert for postgres
def insert_video(userName, actualName, uploadTime, uploadString, viewString, viewCount, videoId, link, subCount, videoTitle, country):
	with conn:
		c.execute("""INSERT INTO uploadData (userName, actualName,  uploadTime, 
			uploadString, viewString, viewCount, videoId, link, subCount, videoTitle, country) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)""", 
			(userName, actualName, uploadTime, uploadString, viewString, viewCount, videoId, link, subCount, videoTitle, country))




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

def excelUpload():


	def query_all():
		c.execute("SELECT * FROM moredata")
		return c.fetchall()


	youtubeUsernames1 = query_all()
	youtubeUsernames = [x[0] for x in youtubeUsernames1]

	country = [x[2] for x in youtubeUsernames1]
	#print(youtubeUsernames)



	#import list of youtubers
	#importing spreadsheet
	#df = pd.read_excel('listofyoutubers.xlsx', sheet_name='Sheet1')

	#get columns
	#columns = df.columns
	#columns2 = np.asarray(columns)
	#print("Column headings: ", columns2)

	#get rows. delete nan rows
	#listOfYoutubers = (df['USERNAME'].dropna()).as_matrix()
	#youtubeUsernames = np.asarray(listOfYoutubers)
	#print("Category Rows: ", youtubeUsernames)

	videoPage(youtubeUsernames, country)

def videoPage(youtubeUsernames, country):
	for i in range(len(youtubeUsernames)):

		print("Youtuber: ", youtubeUsernames[i])
		userNameUser = youtubeUsernames[i]
		countryUser = country[i]
		#to incorporate postgres new database need videos, not /videos

		if ("channel/" not in userNameUser):
			browser.get('https://www.youtube.com/user/' + youtubeUsernames[i] + 'videos?sort=dd&shelf_id=0&view=0')
		#browser.get('https://www.youtube.com/user/' + youtubeUsernames[i] + '/videos')
		else:
			browser.get('https://www.youtube.com/' + youtubeUsernames[i] + 'videos?sort=dd&shelf_id=0&view=0')
		

		try: 
			videoPage = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'alerts')))
			#print("Video page loaded")
			sleep(2)

		except TimeoutException:
			print("Loading video page needs more time to load")
			sleep(7)

		uploadWhen(userNameUser, countryUser)

def uploadWhen(userNameUser, countryUser):

	loop = 0
	isNew = True


	while isNew == True:

		try:

			#make sure not live or set reminder
			#LIVE pushes data from next videos back - uploadstring/ uploadtime is wrong




			#grabbing most recent vid date
			mostRecentVid = browser.find_elements_by_xpath('//div[@id = "metadata-line"]/span[2]')[loop].text
			print("Upload Date: ",mostRecentVid)
			correctedMostRecentVid = mostRecentVid.split()
			#print(correctedMostRecentVid)
			#print(correctedMostRecentVid[0])
			#print(correctedMostRecentVid[1])

			#loop until videos become over 3 days old
			if ((correctedMostRecentVid[1] == 'minute') or (correctedMostRecentVid[1] =='minutes') 
			or (correctedMostRecentVid[1] == 'hour') or (correctedMostRecentVid[1] == 'hours')
			or (correctedMostRecentVid[1] =='day') 
			or (int(correctedMostRecentVid[0]) < 3 and (correctedMostRecentVid[1]) == 'days')):
				#print("new video phase 1")



				daysToMins(correctedMostRecentVid, mostRecentVid, userNameUser, loop, countryUser)
				loop += 1
				isNew = True 

			elif ((correctedMostRecentVid[1] == 'week') or (correctedMostRecentVid[1] == 'weeks') 
			or (correctedMostRecentVid[1] == 'month') or (correctedMostRecentVid[1] == 'months')
			or (correctedMostRecentVid[1] == 'year') or (correctedMostRecentVid[1] == 'years') 
			or (int(correctedMostRecentVid[0]) > 2 and (correctedMostRecentVid[1]) =='days')):
				#print("old video phase 1")
				isNew = False

			else:
				print("couldn't determine upload date")
				isNew = False

		except IndexError:
			isNew = False

		except NoSuchElementException:
			isNew = False

		

def daysToMins(correctedMostRecentVid, mostRecentVid, userNameUser, loop, countryUser):
	#narrow down further by days
	#if (int(correctedMostRecentVid[0]) > 2) and (correctedMostRecentVid[1] == 'days'):
		#print("old video phase 2")

	#else:
		#print("new video phase 2")

		#recalculate so we can search by mins
	if(int(correctedMostRecentVid[0]) == 2) and (correctedMostRecentVid[1] == 'days'):
		fixedUploadTime = 48*60

	elif(int(correctedMostRecentVid[0]) == 1) and (correctedMostRecentVid[1] == 'day'):
		fixedUploadTime = 24*60

	elif(correctedMostRecentVid[1] == 'hour') or (correctedMostRecentVid[1] == 'hours'):
		fixedUploadTime = int(correctedMostRecentVid[0])*60

	else:
		fixedUploadTime = int(correctedMostRecentVid[0])

	insert(mostRecentVid, fixedUploadTime, userNameUser, loop, countryUser)

def insert(mostRecentVid, fixedUploadTime, userNameUser, loop, countryUser):
	#grabbing views
	mostRecentViews = browser.find_elements_by_xpath('//div[@id = "metadata-line"]/span[1]')[loop].text
	print("Views: ",mostRecentViews)

	correctedMostRecentViews = mostRecentViews.split()

	#print(correctedMostRecentViews)
	viewsRecent = numberFix(correctedMostRecentViews[0])
	#print(viewsRecent)

	viewsLIVE = correctedMostRecentViews[1]

	

	print(viewsLIVE)
	if (viewsLIVE == "watching"):
		print("uploadTime and uploadstring are pushed back")
		uploadTime = 00
		uploadString = "live"
		#counter for next vid needs to be pushed back
		

	
	else:
		print("no live event")
		#tuple
		uploadTime = fixedUploadTime
		#print(uploadTime)
		#print(type(uploadTime))
		uploadString = mostRecentVid



	#prepare vars for database
	userName = userNameUser
	#userName = youtubeUsernames[i]
	#print(type(userName))

	country = countryUser

	channelTitle = browser.find_element_by_xpath('//span[@id = "channel-title"]').text
	#print(channelTitle)
	actualName = channelTitle
	#print(type(actualName))

	



	viewString = mostRecentViews

	viewCount = int(viewsRecent)
	#print(type(viewCount))

	#link to video
	linkToVid = browser.find_elements_by_xpath('//a[@id = "thumbnail"]')[loop]\
		.get_attribute('href')
	#print(linkToVid)
	#'https://www.youtube.com/watch?v=oRxwrYvFSN0
	#"https://www.youtube.com/embed/jvO1GDJXOgo"
	link = linkToVid.replace("watch?v=", "embed/")
	#print(type(link))

	videoId = linkToVid.replace("watch?v=","").replace("https://www.youtube.com/", "")

	subscribers = browser.find_element_by_xpath('//div/yt-formatted-string[@id = "subscriber-count"]').text
	subCount = subscribers
	print(subCount)

	title = browser.find_elements_by_xpath('//a[@id="video-title"]')[loop]\
		.get_attribute('title')
	videoTitle = title
	print(videoTitle)

	#"host_language":"en"
	#lang will do later

	#enter to database
	insert_video(userName, actualName, uploadTime, uploadString, viewString, viewCount, videoId, link, subCount, videoTitle, country)




def getUploadData():
	#comment out if running on file db, not memory. add lang later
	c.execute("""CREATE TABLE IF NOT EXISTS uploadData (
			id SERIAL PRIMARY KEY NOT NULL,
			userName text,
			actualName text,
			uploadTime int,
			uploadString text,
			viewString text,
			viewCount int,
			videoId text,
			link text,
			subCount text,
			videoTitle text,
			country text
			)""")

	#import youtube list, run through each one and input to db if uploaded in last 48 hrs
	excelUpload()


#delete entire table
def delete_table(conn, c):
	with conn:
		c.execute("DELETE FROM uploadData")

def replicate():
	with conn: 
		c.execute("CREATE TABLE IF NOT EXISTS replace AS TABLE uploadData")

#just need to delete replace table before next update

def dropReplicate():
	with conn:
		c.execute("DROP TABLE replace")


while True:
	delete_table(conn, c)
	getUploadData()
	dropReplicate()
	replicate()
	#in seconds
	sixHours = 60 * 60 * 6
	time.sleep(sixHours)




c.close()
conn.close()
browser.close()


