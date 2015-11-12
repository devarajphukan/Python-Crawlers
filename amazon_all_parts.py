
import requests
from bs4 import BeautifulSoup
fw = open("amazonPartLinks.txt","r")
 
for i in fw:



	url = i.strip()
	try :
		html = requests.get(url).text

		infoDic = {}
		
		soup = BeautifulSoup(html,"lxml")

		name = soup.find("span",{"id":"productTitle"}).text
		infoDic["name"] = str(name).strip()
		infoDic["url"] = url

		try :
			price = soup.find("span",{"id":"priceblock_ourprice"})
			infoDic["price"] = str(price).split("</span>")[-2].strip()
		except :
			
			continue	

		j = soup.find("div",{"class":"pdTab"}).find("table").find("tbody")
		
		for k in j.find_all("tr") :
			l = k.find_all("td")
			try :

				infoDic[str(l[0].text).strip()] = str(l[1].text).strip()
			except :
				pass

		
		print infoDic
	
	except :

		continue 
