#!/usr/bin/python

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

fo = open("home2","r")
fw = open("data.txt","a")

driver = webdriver.Firefox()
timer = 1
for x in fo :
	
	time.sleep(5)
	
	
	
	print y
	driver.get("http://www.google.com/"+chr(35)+"q="+str(y))
	source_code = driver.page_source
		
	soup = BeautifulSoup(source_code,"lxml")

	c = 1
	
	try :
		i = soup.find('span',{'class':'st'}).text
		
		i=str(filter(lambda x:ord(x)>31 and ord(x)<128,i))
		main_text = i
		fw.write(main_text)
		fw.write("\n")
	except :
		pass

	
	try :	
		for i in soup.find_all('div',{'class':'st'}):
			j = i.text
			
			j=str(filter(lambda x:ord(x)>31 and ord(x)<128,j))
			fw.write(j)
			fw.write("\n")
			c += 1

	except :
		pass
		

	

	d = 0
	try :
		
		for i in soup.find_all('h3',{'class':'r'}):
			if d == c :
				break
			else :
				j = i.find('a').get('href')
				j=str(filter(lambda x:ord(x)>31 and ord(x)<128,j))
			
				fw.write(j)
				fw.write("\n")
				k = i.find('a').text
				k=str(filter(lambda x:ord(x)>31 and ord(x)<128,k))
				fw.write(k)
				fw.write("\n")
				
			d += 1
		
		
	except :
		pass

	
	
	fw.write("\n\n")
	timer += 1


	
