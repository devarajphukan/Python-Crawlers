#!/usr/bin/python
import aiohttp
import asyncio
from bs4 import BeautifulSoup

def get(*a, **k):
	
	response = yield from aiohttp.request("GET", *a, **k)
	return (yield from response.text())


def spider(page):
	
	soup = BeautifulSoup(page,'lxml')
	mylinks = []
	mytags = []
	for link in soup.findAll('img',{'class' : 'preview_img'}):
		image_link = "https://pixabay.com" + link.get('data-url')
		tags = link.get('alt')
		mylinks.append(image_link)
		mytags.append(tags)
	info = zip(mylinks,mytags)
	info = list(info)

	return info

def print_title(query):	
	
	url = "https://pixabay.com/en/photos/?&pagi={}".format(query)
	with (yield from sem):
		page = yield from get(url, compress=True)
	links = spider(page)
	
	for i in range(len(links)):
		print('{}: {} {}'.format(query, links[i][0],links[i][1]))

sem = asyncio.Semaphore(10)
loop = asyncio.get_event_loop()
f = asyncio.wait([print_title(d) for d in range(1,4076)])
loop.run_until_complete(f)
