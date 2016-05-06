#/usr/bin/python 

import requests
import threading
from bs4 import BeautifulSoup

url = "http://www.thinkstockphotos.in"
html_text = requests.get(url)
plain_text = html_text.text
soup = BeautifulSoup(plain_text,'lxml')
soup=soup.find("div",{"class":"left"})
soup = soup.find_all('ul')
dic={}
fw = open("thinkstock","a")
for i in soup :
    
    x = i.find_all('li')
    for j in x :
        y = j.find('a').get('href')
        s = y.split("?")[0]
	
	url_img = "http://www.thinkstockphotos.in"+str(s)
	html = requests.get(url_img).text
	soup1 = BeautifulSoup(html,'lxml')
	soup1 = soup1.find('ul',{'class':'pager'}).find('span',{'class':'totalPages'}).text
	dic["http://thinkstockphotos.in"+str(s)+"?page="]=int(str(soup1).replace(",",""))
print dic

def get_info(url,page_id):
	url1 = url+str(page_id)
	html = requests.get(url1)
	plain = html.text
	soup = BeautifulSoup(plain,'lxml')
	soup = soup.find_all('div',{'class':'result'})
	for divs in soup :
		info = divs.find('a',{'class':'detailLink'})
		info2 = info.find('img').get('preview')
		info3 = info.find('img').get('alt')
		info3=str(filter(lambda x:ord(x)>31 and ord(x)<128,info3))
		fw.write(info2+"\n"+info3+"\n")

print"*********************"

for url,size in dic.items():
	index=0
	while index<int(size):
		while threading.activeCount()<400:
			t=threading.Thread(target=get_info,args=(url,index,))
			t.start()
			index+=1


			
			


