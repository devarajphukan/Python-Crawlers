
from simplejson import loads 
from bs4 import BeautifulSoup
import requests
import threading 

def spider(i) :
	
	try :
		
		html = requests.get("http://www.morguefile.com/affiliate/getty/"+str(i)+"/?sort=pop&photo_lib=Getty")

		json = loads(html.content)

		if len(json.get('response')[0]) > 1 :

			for i in range(20) :

				url = (json.get('response')[i])['ImageURL']
				url = str(filter(lambda x:ord(x)>31 and ord(x)<128,url)).strip()
				title = (json.get('response')[i])['Title']
				title = str(filter(lambda x:ord(x)>31 and ord(x)<128,title)).strip()
				 
		else :

			pass

	except :

		pass

T=threading.Thread		

for j in range(1,100000000) :
	while threading.active_count()>10:
		continue
	t=T(target=spider,args=(j,))
	t.start()
	
