import requests
from bs4 import BeautifulSoup
from xlutils.copy import copy
from xlrd import *
import threading
w = copy(open_workbook('data.xls'))
fw = open("amazonPartLinks.txt","r")
a = 1
links = []

for i in fw:
	links.append(i)

def getInfo(i) :
	url = links[i].strip()
	try :
		html = requests.get(url).text
		product_info = {}
		soup = BeautifulSoup(html,"lxml")
		name = soup.find("span",{"id":"productTitle"}).text
		product_info["name"] = str(name).strip()
		product_info["url"] = url

		try :
			price = soup.find("span",{"id":"priceblock_ourprice"})
			product_info["price"] = str(price).split("</span>")[-2].strip()
		except :
			pass	

		j = soup.find("div",{"class":"pdTab"}).find("table").find("tbody")
		elem = "<br>"
		for k in j.find_all("tr") :
			l = k.find_all("td")
			try :
				elem = elem + str(l[0].text).strip() + " : " + str(l[1].text).strip() + "<br>"
			except :
				pass

		print product_info["name"]
		w.get_sheet(0).write(a,2,product_info["name"])
		w.get_sheet(0).write(a,4,product_info["price"])
		w.get_sheet(0).write(a,15,product_info["url"])
		w.get_sheet(0).write(a,13,elem)
		w.save('amazonAllPart.xls')
		a += 1
		
	except :
		pass

T=threading.Thread		
for m in range(1,len(links)) :
	while threading.active_count()>10 :
		continue
	t=T(target=getInfo,args=(m,))
	t.start()
