#!/usr/bin/python

import threading
import urllib2
from bs4 import BeautifulSoup

def spider(page):	
	url = "https://pixabay.com/en/photos/?&pagi="+str(page)
	source_code = urllib2.urlopen(url)
	plain_text = source_code.read()
 	soup = BeautifulSoup(plain_text,'lxml')
	
	for link in soup.findAll('img',{'class' : 'preview_img'}):
		image_link = "https://pixabay.com" + link.get('data-url')
		prw_link = "https://pixabay.com" + link.get('src')	
		tags = link.get('alt')
		print image_link
		tags=str(filter(lambda x:ord(x)>31 and ord(x)<128,tags))
		f.write(image_link+"\n"+prw_link+"\n"+tags+"\n")
	
T=threading.Thread		
f=open("pixaimage.txt","a")
for i in range(1,4055):
	while threading.active_count()>200:
		continue
	t=T(target=spider,args=(i,)	)
	t.start()
	

