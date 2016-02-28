#!/usr/bin/python
import threading
import requests
from bs4 import BeautifulSoup

def spider(i):
	url = "http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=6bo%2Cb5g&pincode=560036&filterNone=true&start="+str(i)+"&ajax=true&_=1456672233883"
	html_text = requests.get(url)

	plain_text = html_text.text
	soup = BeautifulSoup(plain_text)
	
	try :
	
		for j in soup.find_all("div",{"class":"pu-details lastUnit"}):

			k = j.find("a",{"class":"fk-display-block"}).get("title")
			k = str(k).split("(")[0]
			
			l = j.find("span",{"class":"fk-font-17 fk-bold"}).text
			
			print str(k)
			print str(l)
	
	except :
		pass


T=threading.Thread		

for n in range(1,100000):
	
	while threading.active_count()>2:
		
		continue
	
	t=T(target=spider,args=(n,))
	t.start()
