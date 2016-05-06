import requests
from bs4 import BeautifulSoup
import threading
import pymysql

cat_list = ["animals","party","people","travel","body","professional","news","sports","entertainment","archival","fashion","travel"]

for i in cat_list :
	
	cat_name = i 	
	url1 = "http://www.gettyimages.in/photos/"+str(i)+"?family=editorial&assettype=image&excludenudity=true&mediatype=photography&page=2&phrase="+str(i)+"&sort=mostpopular"

	a = requests.get(url1) 
	b = a.text

	soup1 = BeautifulSoup(b,"lxml")

	i = soup1.find("input",{"type":"number"})
	j = i.get("max")
	j = int(j)
	
	def scraper(pg_num) :

		db = pymysql.connect("localhost","root","Passwd","deviantart")
		cursor = db.cursor()

		url = ("http://www.gettyimages.in/photos/"+str(cat_name)+"?family=editorial&assettype=image&excludenudity=true&mediatype=photography&page="+str(pg_num)+"&phrase="+str(cat_name)+"&sort=mostpopular")
	
		html_text = requests.get(url)
		plain_text = html_text.text 
		soup = BeautifulSoup(plain_text,"lxml")

		try :


			for n in soup.find_all("article",{"class":"asset"}) :

				try :

					j = n.find("section",{"class":"image-section"})
					link = j.get("gi-preview-image")
					#print link

				except :

					link = "None"

				try :

					k = n.find("section",{"class":"image-section"}).find("a").find("img")
					alt = k.get("alt")
					#print alt

				except :

					alt = "None"

				try :

					l = n.find("section",{"class":"image-section"}).find("a").find("img")
					prvw = l.get("src")
					#print prvw

				except :

					prvw = "None"  
				
				

				insert_sql = "INSERT INTO `images` (`img_link`,`img_preview`,`img_title`) VALUES ('%s','%s','%s')" %(link,prvw,alt)
				cursor.execute(insert_sql)
				db.commit()
		
		except :

			pass

	T=threading.Thread		
	for m in range(1,j) :
		while threading.active_count()>15 :
			continue
		t=T(target=scraper,args=(m,))
		t.start()
