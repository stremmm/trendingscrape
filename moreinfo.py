import os

#import sqlite3

import psycopg2

import pandas as pd
import requests
import time
from time import sleep
import numpy as np
import json



#youtubeLocation auth
#key = AIzaSyBnddFlIiwqyuSo8vJSM10m1yTRfDeA1As

DEVELOPER_KEY = "AIzaSyCIG5h0eVZPmdoYqKdU8O2zydb5RYtPXPs"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
BASE = "https://www.googleapis.com/youtube/v3/channels"


#starting db with postgres on local comp
conn = psycopg2.connect(host="localhost", database="youtubedb", user="", password="")

#executes sql commands on both sqlite3 and postgres
c = conn.cursor()
print("connected to db")





#insert for postgres
def insert_video(userName, adjustUserName, country):
	with conn:
		c.execute("""INSERT INTO moreData (userName, adjustUserName, country) VALUES (%s, %s, %s)""", 
			(userName, adjustUserName, country))



def videoPage(youtubeUsernames):
	for i in range(len(youtubeUsernames)):

		userName = youtubeUsernames[i]

		adjustUserName = youtubeUsernames[i].replace("/","")

		print("Youtuber: ", adjustUserName)
		PARAMS = {'part': 'snippet', 'forUsername': adjustUserName, "key": 'AIzaSyCIG5h0eVZPmdoYqKdU8O2zydb5RYtPXPs'}

		r = requests.get(url = BASE, params = PARAMS)

		json_data = r.json()
		#print(json_data)

		#write exception

		try:
			country = json_data['items'][0]['snippet']['country']
			print(country)

			insert_video(userName, adjustUserName, country)

		except:
			country = 'NA'
			print(country)
			insert_video(userName, adjustUserName,country)







def getCountry():
	def query_all():
		c.execute("SELECT * FROM scrapeData")
		return c.fetchall()

	youtubeUsernames1 = query_all()
	youtubeUsernames = [x[0] for x in youtubeUsernames1]

	videoPage(youtubeUsernames)


def toDb():
	c.execute("""CREATE TABLE IF NOT EXISTS moreData (
		userName text,
		adjustUserName text,
		country text
		)""")

	getCountry()


#delete entire table
def delete_table(conn, c):
	with conn:
		c.execute("DELETE FROM moredata")




delete_table(conn,c)

#run entire with
toDb()


