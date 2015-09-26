from simplejson import loads 
from bs4 import BeautifulSoup
import requests
import threading 

fobj = open("dreamstimeTracker","a")
fw = open("dreamstime.txt","a")

def spider(i) :
	

	html = requests.get("http://www.morguefile.com/affiliate/dreamstime/"+str(i)+"/?sort=pop&photo_lib=Dreamstime")

	json = loads(html.content)

	a = (json['result'])
	
	try :
		
		b = (a['items'])
		c = (b['item'])
		
		print i 

		for i in range(20) :

			dict = {}

			try :

				url =  (c[i])['largeThumb']
				url = str(filter(lambda x:ord(x)>31 and ord(x)<128,url)).strip()
				dict['url'] = url
				
				title = (c[i])['title']
				title = str(filter(lambda x:ord(x)>31 and ord(x)<128,title)).strip()
				dict['title'] = title 
				
				fw.write(str(dict))
			
			except :
				pass
	
	except :

		fobj.write(str(i)+'\n')
		pass 



T=threading.Thread		

for j in range(1,1000000) :
	while threading.active_count()>10 :
		continue
	t=T(target=spider,args=(j,))
	t.start()
	
