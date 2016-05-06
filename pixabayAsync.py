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
	
	info = list(zip(mylinks,mytags))

	return info

def print_link_tags(page_num):	
	
	url = "https://pixabay.com/en/photos/?&pagi={}".format(page_num)
	
	with (yield from sem):
		page = yield from get(url, compress=True)
	
	links = spider(page)
	
	for i in range(len(links)):
		print('{}: {} {}'.format(page_num, links[i][0],links[i][1]))

sem = asyncio.Semaphore(10)
loop = asyncio.get_event_loop()
f = asyncio.wait([print_link_tags(d) for d in range(1,4100)])
loop.run_until_complete(f)
