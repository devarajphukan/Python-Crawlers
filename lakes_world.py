
import requests
from bs4 import BeautifulSoup

root_url = "http://www.iaglr.org/lakes/list/all/"
html_text = requests.get(root_url)
plain_text = html_text.text 

links = []
lakeName = []
countries = []
surfaceAreas = []
types = []

soup = BeautifulSoup(plain_text,"lxml")

i = soup.find("ul",{"id":"byalpha"})

for j in i.find_all("li") :

	k = j.find("a").get("href")
	links.append(str(k))
	l = j.find("a").text
	l=str(filter(lambda x:ord(x)>31 and ord(x)<128,l)) 
	lakeName.append(str(l).strip())

for l in links :

	url = "http://www.iaglr.org"+l 
	html_text = requests.get(url)
	plain_text = html_text.text 

	soup = BeautifulSoup(plain_text,"lxml")
	
	i = soup.find("table",{"summary":"Lake Data"})

	for i in soup.find_all("tr") :
		
		
		j = str(i.find("th").text)
		
		try :

			if j == "Country (State, Province, or Territory)" :

				Country = str(i.find("td").text)
				countries.append(Country)
		except :

				countries.append("N.A") 
		
		try :

			if j == "Surface Area (km2)" :
				Area = str(i.find("td").text).split(" ")[0].strip()
				surfaceAreas.append(Area)

		except :

				surfaceAreas.append("N.A") 
		
		try :

			if j == "Fresh/Salt" :

				Type = str(i.find("td").text)
				types.append(Type)
		except :

				types.append("N.A")

	print l
	
print len(countries)
print len(lakeName)
print len(surfaceAreas)
print len(types)		
