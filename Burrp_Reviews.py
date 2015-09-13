#!/usr/bin/python
from simplejson import loads 
from bs4 import BeautifulSoup
import requests

fw = open("BBqNationReviews","w")

for i in range(10000):

	html = requests.get("http://www.burrp.com/bangalore/listings/getmorereviews?start="+str(i)+"&post_id=2749&post_type=ESTABLISHMENT&shareUrl=http%3A%2F%2Fwww.burrp.com%2Fbangalore%2Fbarbeque-nation-hal-2nd-stage-listing%2F2749&sort=latest&user_id=&estname=Barbeque+Nation")
		

	json = loads(html.content)
	
	if json.get('status'):
		
		
		soup =  BeautifulSoup(json.get('result'),'lxml')
		
		t = soup.find('p',{'id':'title'})
		ttl = t.text
		ttl=str(filter(lambda x:ord(x)>31 and ord(x)<128,ttl))
		
		
		rw = soup.find('p',{'id':'body'})
		rvw = rw.text
		rvw=str(filter(lambda x:ord(x)>31 and ord(x)<128,rvw))

		rt = soup.find('span',{'class':'star59x55 FR'})
		j = rt.text
		k = float(j)
		
		print k
	
	else:
		
		print "break"
		
		break


	fw.write(ttl)
	fw.write(rvw)
	fw.write(k)
	fw.write("\n")
