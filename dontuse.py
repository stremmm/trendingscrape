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

import datetime

#start session in chrome on local server
#if want to use headless
#browser = webdriver.Chrome('./assets/chromedriver', chrome_options=options)
#if want to see chrome
#browser = webdriver.Chrome('./assets/chromedriver')

#start session in chrome on CLOUD SERVER
#browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)


#starting database with sqlite3
#two options to store:
##1 - in memory - lives in ram. good for testing. starts from scratch
#conn = sqlite3.connect(':memory:')
##2 - in file. creates file or connects to it
#conn = sqlite3.connect('burstDB.db')

#starting db with postgres on local comp
conn = psycopg2.connect(host="localhost", database="loginauth", user="", password="")

#executes sql commands on both sqlite3 and postgres
c = conn.cursor()
print("connected to db")




def submitOrder():
	#comment out if running on file db, not memory. add lang later
	c.execute("""CREATE TABLE IF NOT EXISTS orders (
			orderNumber int PRIMARY KEY NOT NULL UNIQUE,
			username text NOT NULL references customerInfo(username),
			paymentMethod text NOT NULL,
			totalprice numeric(9,2 ) NOT NULL,
			orderDate DATE NOT NULL,
			
			
			shippingPrice numeric(7,2 ) NOT NULL,
			discountPrice numeric(7,2 ) NOT NULL,
			discountCode text references discountcode(discountCode)
			)""")



#submitOrder()


#paymentMethod = "Credit Card"
#orderDate = datetime.date.today()
#username = 'stephstrem'
#orderNumber = 1000
#totalprice = 150.00

#shippingPrice = 7.99
#discountPrice = 30.00
#discountCode = "SAVE 20"


#insert for postgres
def insert_order(orderNumber, username, paymentMethod, totalprice, orderDate, shippingPrice, discountPrice, discountCode):
	with conn:
		c.execute("""INSERT INTO orders (orderNumber, username, paymentMethod, totalprice, orderDate, shippingPrice, discountPrice, discountCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
			(orderNumber, username, paymentMethod, totalprice, orderDate, shippingPrice, discountPrice, discountCode))



#insert_order(orderNumber, username, paymentMethod, totalprice, orderDate, shippingPrice, discountPrice, discountCode)











def submitCoupon():
	#comment out if running on file db, not memory. add lang later
	c.execute("""CREATE TABLE IF NOT EXISTS discountcode (
			discountCode text PRIMARY KEY NOT NULL,
			description text NOT NULL,
			codeType text NOT NULL,
			upc int NOT NULL references products(upc),
			percentOff int,
			dollarOff numeric(7,2 ),
			conditions numeric(7,2 ),
			modifiedDate DATE NOT NULL

			)""")

#submitCoupon()



#discountCode = "SAVE 20"
#description = "For orders over 50, get 20 percent off"
#codeType = "percent"
#upc = 95555555
#percentOff = 20
#dollarOff = 0
#onditions = 50
#modifiedDate = datetime.date.today()



#insert for postgres
def insert_code(discountCode, description, codeType, upc, percentOff, dollarOff, conditions, modifiedDate):
	with conn:
		c.execute("""INSERT INTO discountcode (discountCode, description, codeType, upc, percentOff, dollarOff, conditions, modifiedDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
			(discountCode, description, codeType, upc, percentOff, dollarOff, conditions, modifiedDate))



#insert_code(discountCode, description, codeType, upc, percentOff, dollarOff, conditions, modifiedDate)














def updateProducts():
	#comment out if running on file db, not memory. add lang later
	c.execute("""CREATE TABLE IF NOT EXISTS products (
			upc int PRIMARY KEY NOT NULL,
			item text NOT NULL,
			brand text NOT NULL,
			category text NOT NULL		
			)""")




#updateProducts()

#upc = 95555555
#item = "Corsair K95 Gaming Keyboard"
#brand = "Corsair"
#category = 'electronics'

#upc= 90102033
#item = "Logitech G502 RGB Gaming Mouse"
#brand="Logitech"
#category = "electronics"


#insert for postgres
def insert_products(upc, item, brand, category):
	with conn:
		c.execute("""INSERT INTO products (upc, item, brand, category) VALUES (%s, %s, %s, %s)""", 
			(upc, item, brand, category))



#insert_products(upc, item, brand, category)







def updateInventory():
	#comment out if running on file db, not memory. add lang later
	c.execute("""CREATE TABLE IF NOT EXISTS inventory (
			upc int PRIMARY KEY NOT NULL references products(upc),
			quantSold int NOT NULL,
			quantAvailable int NOT NULL,
			modifiedDate DATE NOT NULL
			)""")

#updateInventory()

#upc = 95555555
#quantSold = 0
#quantAvailable = 55
#modifiedDate = datetime.date.today()



#upc = 90102033
#quantSold = 0
#quantAvailable = 80
#modifiedDate = datetime.date.today()

#insert for postgres
#def insert_inventory(upc, quantSold, quantAvailable, modifiedDate):
	with conn:
		c.execute("""INSERT INTO inventory (upc, quantSold, quantAvailable, modifiedDate) VALUES (%s, %s, %s, %s)""", 
			(upc, quantSold, quantAvailable, modifiedDate))



#insert_inventory(upc, quantSold, quantAvailable, modifiedDate)



#update account info

def updateCustomerInfo():
	#comment out if running on file db, not memory. add lang later
	c.execute("""CREATE TABLE IF NOT EXISTS customerInfo (

			username text PRIMARY KEY NOT NULL,
			email text NOT NULL,
			firstname text,
			lastname text,
			phonenumber text,
			modifiedDate DATE NOT NULL	
			)""")

#updateCustomerInfo()

#username = "stephstrem"
#email = "stremick1@hotmail.com"
#firstname = "stephanie"
#lastname = "stremick"
#phonenumber = 3039059261
#modifiedDate = datetime.date.today()



#insert for postgres
def insert_customerInfo(username, email, firstname, lastname, phonenumber, modifiedDate):
	with conn:
		c.execute("""INSERT INTO customerInfo (username, email, firstname, lastname, phonenumber, modifiedDate) VALUES (%s, %s, %s, %s, %s, %s)""", 
			(username, email, firstname, lastname, phonenumber, modifiedDate))



#insert_customerInfo(username, email, firstname, lastname, phonenumber, modifiedDate)





#update picture paths
def updateImages():
	#comment out if running on file db, not memory. add lang later
	c.execute("""CREATE TABLE IF NOT EXISTS imagepath (
			count SERIAL NOT NULL,
			upc int NOT NULL references products(upc),
			image text NOT NULL,
			modifiedDate DATE NOT NULL,
			PRIMARY KEY (upc,count)
			)""")

#updateImages()

#upc = 95555555
#image = "corsair.jpg"

#image = "corsair1.jpg"
#image = "logitech.jpg"
#image= "logitech1.jpg"
#modifiedDate = datetime.date.today()



#insert for postgres
def insert_images(upc, image, modifiedDate):
	with conn:
		c.execute("""INSERT INTO imagepath (upc, image, modifiedDate) VALUES (%s, %s, %s)""", 
			(upc, image, modifiedDate))



#insert_images(upc, image, modifiedDate)








#update price
def updatePrice():
	#comment out if running on file db, not memory. add lang later
	c.execute("""CREATE TABLE IF NOT EXISTS priceProduct (
			count SERIAL NOT NULL,
			upc int NOT NULL references products(upc),		
			price numeric(7,2 ) NOT NULL,
			msrp numeric (7,2) NOT NULL,
			modifiedDate DATE NOT NULL,
			PRIMARY KEY (upc, count) 

			)""")

#updatePrice()

#upc = 95555555
#price = 45.00
#msrp = 75.00
#modifiedDate = datetime.date.today()

#upc = 90102033
#price = 80.00
#msrp = 100.00
#modifiedDate = datetime.date.today()



#insert for postgres
def insert_price(upc, price, msrp, modifiedDate):
	with conn:
		c.execute("""INSERT INTO priceProduct (upc, price, msrp, modifiedDate) VALUES (%s, %s, %s, %s)""", 
			(upc, price, msrp, modifiedDate))



#insert_price(upc, price, msrp, modifiedDate)





#update price
def updateProdOrder():
	#comment out if running on file db, not memory. add lang later
	c.execute("""CREATE TABLE IF NOT EXISTS orderByProduct (
			ordernumber int NOT NULL references orders(orderNumber),
			username text NOT NULL,
			upc int NOT NULL references products(upc),	
			price numeric(7,2 ) NOT NULL,
			pricequant numeric(7,2 ) NOT NULL,
			quantity int NOT NULL,
			orderDate DATE NOT NULL,
			PRIMARY KEY(ordernumber, upc)
			)""")

updateProdOrder()

ordernumber = 1000
upc = 95555555
quantity = 2
price = 130.00



orderDate = datetime.date.today()
username = 'stephstrem'

pricequant = quantity * price

#insert for postgres
def insert_prodOrder(ordernumber, username, upc, price, pricequant, quantity, orderDate):
	with conn:
		c.execute("""INSERT INTO orderByProduct (ordernumber, username, upc, price, pricequant, quantity, orderDate) VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
			(ordernumber, username, upc, price, pricequant, quantity, orderDate))



insert_prodOrder(ordernumber, username, upc, price, pricequant, quantity, orderDate)

