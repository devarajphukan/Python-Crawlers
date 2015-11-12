import requests
from bs4 import BeautifulSoup
from xlutils.copy import copy
from xlrd import *
w = copy(open_workbook('data.xls'))
a = 1

for i in range(1,13) :

	try :

		url = "http://www.jazzmyride.com/index.php?route=product/search&filter_name=gabriel&page="+str(i)+"&_=1446590318759"
		html = requests.get(url).text
		soup = BeautifulSoup(html,"lxml")

		li = soup.find_all("div",{"class":"product-inner"})

		for j in range(len(li)) :

			try :

				url = li[j].find("h4",{"class":"name"}).find("a").get("href")
				
				name = li[j].find("h4",{"class":"name"}).find("a").text
				name = str(name).strip()
				
				html = requests.get(url).text
				soup = BeautifulSoup(html,"lxml")

				sku = soup.find("span",{"class":"product_code_value"}).text
				sku = str(sku).strip().lower()
				
				manufacturer = "Gabriel"
				category = "Shock Absorbers"
				try :

					price = soup.find("span",{"class":"price-new"}).text
					price = str(price).split(".")[1].replace(",","").strip()
					price = "Rs." + str(int(price) - 100)

				except :

					price = soup.find("span",{"class":"price-old"}).text
					price = str(price).split(".")[1].replace(",","").strip()
					price = "Rs." + str(int(price) - 100)
					
				tabs = soup.find_all("div",{"class":"tab-content"})
				tabs = tabs[1].find("tbody").find_all("tr")

				brand = tabs[0].find_all("td")[1].text
				brand = str(brand).strip()

				car = tabs[1].find_all("td")[1].text
				car = str(car).strip()

				w.get_sheet(0).write(a,1,sku)
				w.get_sheet(0).write(a,2,name)
				w.get_sheet(0).write(a,4,price)
				w.get_sheet(0).write(a,8,manufacturer)
				w.get_sheet(0).write(a,9,category)
				w.get_sheet(0).write(a,11,brand)
				w.get_sheet(0).write(a,14,car)
				w.get_sheet(0).write(a,15,url)
				w.save('Gabriel.xls')

				print a 
				a += 1


			except :

				continue

	except :

		continue
