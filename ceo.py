#!/usr/bin/python
import requests
from bs4 import BeautifulSoup

l1 = ['a-f','g-l','m-r','s-z']
a = 0
names = []
company_name = []
company_link = []

for i in range(3) :

	html_text = requests.get("http://cecp.co/membership/members/members-"+l1[i]+".html")
	print a
	plain_text = html_text.text 

	soup = BeautifulSoup(plain_text,"lxml")
		
	for i in soup.find_all("p",{"class":"ceoName"}):
		try :
			j = i.find("strong").text
			j=str(filter(lambda x:ord(x)>31 and ord(x)<128,j)).strip() 
			names.append(j)

		except :

			pass

	for i in soup.find_all("p",{"class":"MemberCompanyName"}):
		try :
		
			j = i.find("strong").find("a").get("href")
			j=str(filter(lambda x:ord(x)>31 and ord(x)<128,j)).strip()
		
			company_link.append(j)

		except :

			pass

		try :
		
			k = i.find("strong").find("a").text
			k=str(filter(lambda x:ord(x)>31 and ord(x)<128,k)).strip() 
			company_name.append(k)
		except :

			pass

		 
	a += 1
	
final = (zip(company_name,names,company_link))

print final
