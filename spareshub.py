import requests
from bs4 import BeautifulSoup

for page_num in range(1,7) :

	url = "http://spareshub.com/manufacturers/ngk.html?p=" + str(page_num)
	html = requests.get(url)
	plain_text = html.text 
	
	soup = BeautifulSoup(plain_text,"lxml")

	ul = soup.find("ul",{"class" : "products-grid category-products-grid itemgrid itemgrid-adaptive itemgrid-5col single-line-name centered hover-effect equal-height size-s"})

	for li in ul.find_all("li") :

		product_info = {}

		try :
			url = li.find("h2",{"class":"product-name"}).find("a").get("href")
			name = li.find("h2",{"class":"product-name"}).find("a").text.split("From")
			manufacturer = str(name[1].strip())
			name = str(name[0].strip())
			price = str(li.find("div",{"class":"price-box"}).find("span",{"class":"regular-price"}).find("span",{"class":"price"}).text.strip())
			product_info["name"] = name 
			product_info["manufacturer"] = manufacturer
			product_info["price"] = price 

			html = requests.get(url)
			plain_text = html.text
			soup = BeautifulSoup(plain_text,"lxml")

			j = soup.find("table",{"id":"product-attribute-specs-table"}).find_all("td")

			try :
				car = str(j[1]).split(">")[1].split("<")[0]
				product_info["car"] = car
			except :
				product_info["car"] = "-"

			try :
				brand = str(j[4]).split(">")[1].split("<")[0]
				product_info["brand"] = brand
			except :
				product_info["brand"] = "-"

			try :
				category = str(j[6]).split(">")[1].split("<")[0]
				product_info["category"] = category
			except :
				product_info["category"] = "-"

			try :
				oes_number = str(j[7]).split(">")[1].split("<")[0]
				product_info["oes_number"] = oes_number
			except :
				product_info["oes_number"] = "-"


			if "spark" in product_info["category"].lower() :
				print product_info
				#can be inserted to a mongo database as json

			else :
				
				pass 
		except :

			continue
				
