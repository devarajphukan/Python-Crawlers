#!/usr/bin/python
import pymongo
import requests
from bs4 import BeautifulSoup

client=pymongo.MongoClient("192.168.101.5")
db=client.kbnew
lakes=db.lakes


html_text = requests.get("http://www.mapsofindia.com/maps/india/lakemap.htm")
plain_text = html_text.text 

soup = BeautifulSoup(plain_text,"lxml")

i = soup.find("table",{"class":"tableizer-table"})
head_list = ["Lake Name","River Name","Type","Surface Area","Location","State Name"]
info_list = []
b = []
c = []
for i in soup.find_all("tr"):

	info_list = []
	try :

		for j in i.find_all("td"):
			
			j = str(j.text)
			j = " "+j+" "			
			info_list.append(j)

	except :

		continue
	
	a = zip(head_list,info_list)

	b.append(a)

for i in range(len(b)):
	
	c.append(dict(b[i]))

for i in range(len(c)):
	
	disp_order = []
	c[i] = {key: value for key, value in c[i].items() if value != " N.A "}
	
	for j in range(len(head_list)):

		if head_list[j] in c[i].keys() :
			a = head_list[j]
			disp_order.append(a)

	c[i]['display_order'] = disp_order
	lakes.insert(c[i])
