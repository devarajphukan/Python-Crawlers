from bs4 import BeautifulSoup
import requests

urls = ['https://maxiparts.com.au/accessories-and-consumables/automotive/adblue/adblue-filter/','https://maxiparts.com.au/accessories-and-consumables/automotive/adblue/adblue-pumps/','https://maxiparts.com.au/accessories-and-consumables/automotive/bug-deflectors/bracket-kits/']
fw = open('maxiParts.csv','w')
for links in urls :

	try :
		url = links.strip()

		html = requests.get(url).text

		soup = BeautifulSoup(html,'lxml')

		for product in soup.find_all("div",{"class":"ty-product-list__info"}) :
			
			try :
				
				name = product.find('div',{'class':'ty-product-list__item-name'}).find('').text

				price_li = []
				price = product.find('div',{'class':'ty-product-list__price'}).find_all('span')#,{'class':'ty-price-num'}).find('span').text
				
				for i in price :
					
					try :
						pr = price_li.append(float(i.text))
					except :
						continue
				
				catg1 = url.split('/')[3]
				catg2 = url.split('/')[4]

				if len(price_li) == 2 :
					res = catg1,',',catg2,',',name,',',str(price_li[0]),',',str(price_li[1])
					try :
						fw.write(str(res)+'\n')
					except :
						print 'WRITE ERR'
					print res 
				else :
					res = catg1,',',catg2,',',name,',',str(price_li[0])
					try :
						fw.write(str(res)+'\n')
					except :
						print 'WRITE ERR'
					print res 
			except :
				print "E"
	except :
		print "Conn ERR"
