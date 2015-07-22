#/usr/bin/python

import requests
from bs4 import BeautifulSoup
mylist=[]
fw = open("viooz.txt","a")
html_text = requests.get("http://viooz.ac/genre/")
plain_text = html_text.text
soup = BeautifulSoup(plain_text,'lxml')
for i in soup.find_all('td'):
	info = i.find('a').get('href')
	mylist.append("www.viooz.ac"+info+"page/")
		
print mylist
	
for j in range(0,25):
	page_count = 1
	while True:
	
		html_text1 = requests.get("http://"+str(mylist[j])+str(page_count)+"/")
		if (html_text1.status_code == 404):
			break
		
		else :
			plain_text1 = html_text1.text
			soup1 = BeautifulSoup(plain_text1,'lxml')
			for k in soup1.find_all('h3',{'class':'title_grid'}):
				info1 = k.get('title')
				info1=str(filter(lambda x:ord(x)>31 and ord(x)<128,info1))
				print info1
				fw.write(info1+"\n")
		page_count += 1
	print("++++++++++++++++++++++++++++\n")
