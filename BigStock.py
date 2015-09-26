from simplejson import loads 
from bs4 import BeautifulSoup
import requests
import threading 

fobj = open("bigstockTracker","a")
fw = open("bigstockImages.txt","a")

def spider(i) :


	try :

		
		html = requests.get("http://www.morguefile.com/affiliate/bigstock/"+str(i)+"/?sort=pop&photo_lib=Bigstock")
		

		json = loads(html.content)
		

		if (json['results']) :

			print i 

			for i in range(41) :
				dict = {}

				try :
					
					j = (json['results'])[i]
					url = j['img']
					url = str(filter(lambda x:ord(x)>31 and ord(x)<128,url)).strip()
					dict['url'] = url
					title = j['desc']
					title = str(filter(lambda x:ord(x)>31 and ord(x)<128,title)).strip()
					dict['title'] = title
					print str(dict)
					fw.write(str(dict)+"\n")

				except :

					pass 

		else :
			
			pass
		

	except :
		
		fobj.write(str(i)+'\n') 
		pass
	

T=threading.Thread		

for j in range(1,1000000) :
	while threading.active_count()>20:
		continue
	t=T(target=spider,args=(j,))
	t.start()
	
