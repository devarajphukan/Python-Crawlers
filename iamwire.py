import requests
from bs4 import BeautifulSoup
import pymongo
import time

client=pymongo.MongoClient("localhost")
db=client.iamwire
posts=db.posts
authors = db.authors

catList = ["technology","culture","business"]

for categories in catList :

	for b in range(1,100000) :
		
		url = "http://www.iamwire.com/category/"+str(categories)+"/page/"+str(b)
		html = requests.get(url)
		#print html

		if html.status_code == 404 :

			break 

		else :

			plain_text = html.text 
			soup = BeautifulSoup(plain_text,"lxml")

			articles_list = []

			for articles in soup.find_all("h2",{"class":"entry-title"}) :

				a = articles.find("a").get("href")
				a = str(filter(lambda x:ord(x)>31 and ord(x)<128,a)).strip()
				articles_list.append(a) 
			
			for urls in articles_list :

				a = requests.get(urls)
				b = a.text
				soup = BeautifulSoup(b,"lxml")

				main_dict={}

				post_content = {}

				main_dict["source_domain"] = "http://www.iamwire.com"
				main_dict["source_url"] = urls 

				try :

					main_title = soup.find("h1",{"class":"entry-title"}).text
					main_title = str(filter(lambda x:ord(x)>31 and ord(x)<128,main_title)).strip()
					#print "\n",main_title
					main_dict["post_title"] = main_title

				except :
					
					pass
					

				try :

					date = soup.find("time",{"class":"entry-date"}).text
					date = str(filter(lambda x:ord(x)>31 and ord(x)<128,date)).strip()
					#print date 
					date1 = date 
					main_dict["publish_date_string"] = date1 
					b = date.replace(",","").split()
					c = b[0].lower()[:3]
					date = c+" "+b[1]+" "+b[2][-2:]
					date = str(time.mktime(time.strptime(date,"%b %d %y")))
					#print date 
					main_dict["publish_date_unix_epoch"] = date


				except :
					
					pass


				#print "\n"
				try :

					articleTypesList = []
					articleTypes = soup.find("span",{"class":"categories"})
					for atyps in articleTypes.find_all("a") :

						ats = atyps.text
						ats = str(filter(lambda x:ord(x)>31 and ord(x)<128,ats)).strip()
						articleTypesList.append(ats)

					post_content["articleTypeTags"] = articleTypesList
					#print articleTypesList

				except :

					pass



				text_element_list = []

				try :
					
					i = soup.find("div",{"class":"entry-content"})
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
				#print text_element_list


				img_links = []

				try :

					i = soup.find("div",{"class":"entry-content"})
					
					for j in i.find_all("img") :
						
						img_dic = {}
						
						try :

							k = j.get("src")
							k = str(filter(lambda x:ord(x)>31 and ord(x)<128,k)).strip()
							img_dic["url"] = k

							l = j.get("alt")
							l = str(filter(lambda x:ord(x)>31 and ord(x)<128,l)).strip()
							img_dic["alt"] = l 
							img_dic["type"] = "image"
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

					taglist = soup.find("ul",{"class":"tag-list"})
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

					auth_name = soup.find("a",{"class":"url fn n"}).text
					auth_name = str(filter(lambda x:ord(x)>31 and ord(x)<128,auth_name)).strip()
					#print auth_name
					#print "\n"
					auth_dict["full_name"] = auth_name

				except :
					pass


				try :

					abt_auth = soup.find("div",{"class":"author-description"}).find("p").text 
					abt_auth =str(filter(lambda x:ord(x)>31 and ord(x)<128,abt_auth)).strip()
					#print abt_auth
					auth_dict["bio"] = abt_auth

				except :
					pass

				try :

					auth_url = soup.find("div",{"class":"author-link"}).find("a").get("href")
					auth_url =str(filter(lambda x:ord(x)>31 and ord(x)<128,auth_url)).strip()
					#print auth_url
					auth_dict["author_url"] = auth_url
				except :
					pass

				print urls
				#print main_dict
				authors.update({'full_name':auth_name},{'bio':abt_auth,'full_name':auth_name},True)
				auth_ret = authors.find({'full_name':auth_name})
				auth_id = list(auth_ret)
				main_dict["author_id"] = auth_id[0]['_id']

				posts.insert(main_dict)

