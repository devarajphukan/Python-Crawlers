from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()
browser.set_window_size(1366,768)
f = open('petrol_passenger_links.txt')
f1 = open('part_properties.txt','a')
count_car = 0
count_part = 0
for line in f :
	
	line = line.strip().split(',')
	url = line[-1]
	url = url + "?country=IN"
	for part_num in range(10000) :

		try :
			
			browser.get(url)
			time.sleep(3)

			tab = browser.find_element_by_class_name('tab12')
			pt = tab.find_elements_by_class_name('top')
			pt[-1].click()

			div = browser.find_element_by_id('equipment-tab-0')
			tbl = div.find_element_by_tag_name('table')


			tbdy = tbl.find_element_by_tag_name('tbody')
			trs = tbdy.find_elements_by_tag_name('tr')
			tds = trs[part_num].find_elements_by_tag_name('td')

			if len(tds) > 1 :
				info_dic = {'vehicle_type':'passenger','drive_type':'petrol'}
				info_dic['vehicle_make'] = line[0]
				info_dic['vehicle_model'] = line[1]

				info_dic['part_name'] = str(tds[0].text).strip()
				# print info_dic
				tds[0].click()
				time.sleep(3)
				
				a = browser.find_elements_by_class_name('top')
				time.sleep(3)

				for i in a :

					try :
						
						tg_name = i.find_element_by_tag_name('span').text
						if tg_name.strip() == "Description" :
							i.click()
							time.sleep(3)
							ps = browser.page_source
							soup = BeautifulSoup(ps,'lxml')
							tbl_in = soup.find('table')
							prop_dic = {}
							for trr in tbl_in.find_all('tr') :
								try :
									td_tmp = trr.find_all('td')
									prop_dic[td_tmp[0].text] = td_tmp[1].text
								except :
									pass

							info_dic['properties_dic'] = prop_dic

						elif tg_name.strip() == "Comparisons" :
							i.click()
							time.sleep(3)

							ps = browser.page_source
							soup = BeautifulSoup(ps,'lxml')
							tbl_in = soup.find('table')
							comp_dic = {}
							for trr in tbl_in.find_all('tr') :
								try :
									td_tmp = trr.find_all('td')
									comp_dic[td_tmp[0].text] = td_tmp[1].text
								except :
									pass

							info_dic['comparision_dic'] = comp_dic
						else :
							continue


					except :
						continue
				f1.write(str(info_dic).strip() + '\n')
				count_part += 1
				print count_part," parts scraped."
				
			else :
				continue
		except :
			break
	count_car+= 1
	print count_car," cars scraped."