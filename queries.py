
#TO DO 
	#REMOVE DUPES
	




import os

#import sqlite3

import psycopg2

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

#query all data 
def query_all():
		c.execute("SELECT * FROM uploadData")
		return c.fetchall()

#query by most viewed and time limits
def query_by_views_48hr():
		c.execute("SELECT * FROM uploadData ORDER BY viewCount DESC")
		#return c.fetchall()
		#fetch many should be ~100 for official
		return c.fetchmany(5)

def query_by_views_24hr():
		c.execute("SELECT * FROM uploadData WHERE uploadTime < 1441 ORDER BY viewCount DESC")
		#return c.fetchall()
		return c.fetchmany(5)

def query_by_views_12hr():
		c.execute("SELECT * FROM uploadData WHERE uploadTime < 721 ORDER BY viewCount DESC")
		#return c.fetchall()
		return c.fetchmany(5)

def query_by_views_6hr():
		c.execute("SELECT * FROM uploadData WHERE uploadTime < 361 ORDER BY viewCount DESC")
		#return c.fetchall()
		return c.fetchmany(5)


#delete entire table
def delete_table(conn, c):
	with conn:
		c.execute("DELETE FROM uploadData")


print("top 5 - 48 hour")
fortyEightHour = query_by_views_48hr()
print(fortyEightHour)


print("top 5 - 24 hour")
twentyFourHour = query_by_views_24hr()
print(twentyFourHour)

print("top 5 - 12 hour")
twelveHour = query_by_views_12hr()
print(twelveHour)


print("top 5 - 6 hour")
sixHour = query_by_views_6hr()
print(sixHour)




c.close()
conn.close()
