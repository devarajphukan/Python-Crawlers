#!/usr/bin/python
import pymongo 
import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup

client=pymongo.MongoClient("192.168.101.5")
db=client.kbnew
lakes=db.lakes

root_url = "http://www.iaglr.org/lakes/list/all/"
html_text = requests.get(root_url)
plain_text = html_text.text 

links = []

lakeNames = []
countries = []
surfaceAreas = []
types = []

soup = BeautifulSoup(plain_text,"lxml")

i = soup.find("ul",{"id":"byalpha"})

for j in i.find_all("li") :

	k = j.find("a").get("href")
	links.append(str(k))

print ("got links")
print (links)



def get(*a, **k):
	
	response = yield from aiohttp.request("GET", *a, **k)
	return (yield from response.text())

def spider(page,curr_url) :
	
	print (curr_url)
	
	soup = BeautifulSoup(page,"lxml")
	
	j = str(soup.find("div",{"id":"main"}).find("h1").text).strip()
	j = " "+j+" "

	lakeNames.append(j)

	i = soup.find("table",{"summary":"Lake Data"})
	
	

	for i in soup.find_all("tr") :
		
		
		j = str(i.find("th").text)
		
		try :

			if j == "Country (State, Province, or Territory)" :

				Country = str(i.find("td").text).strip()
				Country = " "+Country+" "
				countries.append(Country)
		except :

				countries.append("N.A") 
		
		try :

			if j == "Surface Area (km2)" :
				Area = str(i.find("td").text).split(" ")[0].strip()
				Area = " "+Area+"km^2 "
				surfaceAreas.append(Area)

		except :

				surfaceAreas.append("N.A") 
		
		try :

			if j == "Fresh/Salt" :

				Type = str(i.find("td").text).split(" ")[0].strip()
				Type = " "+Type+" "				
				types.append(Type)
		except :

				types.append("N.A")
		

def le_crawl(l):	
	
	url = "http://www.iaglr.org"+l
	print (url)
	with (yield from sem):
		page = yield from get(url)
	
	spider(page,url)


sem = asyncio.Semaphore(15)
loop = asyncio.get_event_loop()
f = asyncio.wait([le_crawl(d) for d in links])
loop.run_until_complete(f)

info_list = list(zip(lakeNames,countries,surfaceAreas,types))
head_list = ["Lake Name","Country","Surface Area","Type"]

new_list = []

for i in range(len(info_list)):

	j = list(info_list[i])
	new_list.append(j)

for i in range(len(new_list)):

	j = dict(list(zip(head_list,new_list[i])))
	j["display_oreder"] = head_list
	lakes.insert(j)


		
