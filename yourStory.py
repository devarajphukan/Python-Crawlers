import urllib2
from bs4 import BeautifulSoup
import pymongo
import time

client=pymongo.MongoClient("localhost")
db=client.abc
posts=db.posts
authors = db.authors
		
for page_num in range(1,265) :
	
	main_url = "http://yourstory.com/ys-stories/page/"+str(page_num)+"/"
	req = urllib2.Request(main_url, headers={ 'User-Agent': 'Mozilla/5.0' })
	plain = urllib2.urlopen(req).read()

	soup = BeautifulSoup(plain,"lxml")
	#ul = soup.find("ul",{"class":"gridPostsList gridPostsList-fullWidthBlock"})

	url_list =[]
	
	for li in soup.find_all("li",{"class":"grid-full mb-30"}) :
	
		j = li.find("a").get("href")
		j = str(filter(lambda x:ord(x)>31 and ord(x)<128,j)).strip()
		url_list.append(j)

	#print url_list

	for url in url_list :

		a = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
		b = urllib2.urlopen(a).read()
		soup = BeautifulSoup(b,"lxml")
		
		main_dict={}

		post_content = {}

		main_dict["source_domain"] = "http://www.yourstory.com"
		main_dict["source_url"] = url 
		
		try :

			main_title = soup.find("h3",{"class":"title-large color-ys"}).text
			main_title = str(filter(lambda x:ord(x)>31 and ord(x)<128,main_title)).strip()
			#print "\n",main_title
			main_dict["post_title"] = main_title

		except :
			
			pass
			
		
		try :
		
			date = soup.find("p",{"class":"postInfo color-grey mt-5"}).text
			date = str(filter(lambda x:ord(x)>31 and ord(x)<128,date)).strip()
			date1 = date 
			main_dict["publish_date_string"] = date1 
			b = date.replace(",","").split()
			c = b[0].lower()[:3]
			date = c+" "+b[1]+" "+b[2][-2:]
			date = str(time.mktime(time.strptime(date,"%b %d %y")))
			main_dict["publish_date_unix_epoch"] = date
	

		except :
			
			pass

		#print "\n"

		try :

			articleType = soup.find("div",{"class":"pill pill-white mb-16"}).text
			articleType = str(filter(lambda x:ord(x)>31 and ord(x)<128,articleType)).strip()
			post_content["type"] = articleType

		except :

			pass

		text_element_list = []

		try :
			
			i = soup.find("div",{"class":"ys_post_content text"})
			body_text = []

			for j in i.find_all("p") :
				
				
				dic0 = {}

				dic0["el"] = "p"
				dic0["links"] = [] 
				
				text = j.text
				text = str(filter(lambda x:ord(x)>31 and ord(x)<128,text)).strip()
				
				dic0["text"] = text

				try :

					for k in j.find_all("a") :

						page_link_dic = {}
						
						l1 = k.get("href")
						l1 = str(filter(lambda x:ord(x)>31 and ord(x)<128,l1)).strip()
						l2 = k.text 
						l2 = str(filter(lambda x:ord(x)>31 and ord(x)<128,l2)).strip()
						
						page_link_dic["type"] = "page"

						page_link_dic["url"] = l1
						page_link_dic["text"] = l2

						dic0["links"].append(page_link_dic)

				except :

					pass 

				body_text.append(dic0)
			
		except :
			pass

		text_element_list.append(body_text)

		img_links = []

		try :

			i = soup.find("div",{"class":"ys_post_content text"})
			for j in i.find_all("figure") :
				
				img_dic = {}
				img_dic["type"] = "image"
				try :

					k = j.find("a").find("img").get("src")
					k = str(filter(lambda x:ord(x)>31 and ord(x)<128,k)).strip()
					img_dic["url"] = k

					l = j.find("a").find("img").get("alt")
					l = str(filter(lambda x:ord(x)>31 and ord(x)<128,l)).strip()
					img_dic["alt"] = l 
				except :
					pass

				img_links.append(img_dic)

			#print img_links
		except :
			pass

		text_element_list.append(img_links)

		post_content["elements"] = text_element_list

		tags = []

		try :

			taglist = soup.find("ul",{"class":"articleTags mt-5"})
			for i in taglist.find_all("li") :

				j = i.find("a").text
				j = str(filter(lambda x:ord(x)>31 and ord(x)<128,j)).strip()
				tags.append(j)
			#print j	

		except :
			pass

		#print tags
		main_dict["post_tags_list"] = tags 
		#print "\n"
		main_dict["post_content"] = post_content

		auth_dict = {}

		try :

			auth_name = soup.find("a",{"class":"postInfo color-ys"}).text
			auth_name = str(filter(lambda x:ord(x)>31 and ord(x)<128,auth_name)).strip()
			#print auth_name
			#print "\n"
			auth_dict["full_name"] = auth_name

		except :
			pass

		try :

			abt_auth = soup.find("p",{"class":"aboutAuthor_text mt-5"}).text
			abt_auth =str(filter(lambda x:ord(x)>31 and ord(x)<128,abt_auth)).strip()
			#print abt_auth
			auth_dict["bio"] = abt_auth
		
		except :
			pass

		print url
		authors.update({'full_name':auth_name},{'bio':abt_auth,'full_name':auth_name},True)
		auth_ret = authors.find({'full_name':auth_name})
		auth_id = list(auth_ret)
		main_dict["author_id"] = auth_id[0]['_id']

		posts.insert(main_dict)

		
		
