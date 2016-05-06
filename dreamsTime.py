import requests
from bs4 import BeautifulSoup
import MySQLdb
import threading

db = MySQLdb.connect("192.168.101.5","root","PASSWORD","dreamstime")

cursor = db.cursor()

def scraper(page) :

	url = "http://www.dreamstime.com/people_cid114_pg"+str(page)
	html = requests.get(url)
	plain = html.text


	j = plain.split("$(window).bind('load resize', arrangeImages);")[1]
	j = j.split('<script type="text/javascript">')[0].replace("});","").replace("</script>","")
	soup = BeautifulSoup(j,"lxml")
	#print soup
	for i in soup.find_all("div") :
	#print i 

		try :
			j = i.find("a").find("img").get("src")
			j=str(filter(lambda x:ord(x)>31 and ord(x)<128,j))
			#print j
		
		except :
			pass
		
		try :
			
			k = i.find("a").find("img").get("alt")
			k=str(filter(lambda x:ord(x)>31 and ord(x)<128,k))
			#print k
		
		except :
			pass
			insert_sql = "INSERT INTO `images` (`img_link`,`img_title`) VALUES ('%s', '%s')" %(MySQLdb.escape_string(j),MySQLdb.escape_string(k))
			cursor.execute(insert_sql)
			print insert_sql
			db.commit()


T=threading.Thread
for i in range(0,82000) :
	while threading.active_count()>20:
		continue
	t=T(target=scraper,args=(i,))
	t.start()
