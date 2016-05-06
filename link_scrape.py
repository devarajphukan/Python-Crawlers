from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,os

makes = ['ASTON MARTIN','ATUL AUTO LTD','AUDI','BAJAJ AUTO','BENTLEY','BMW','CHEVROLET','DAEWOO','DATSUN', 'FIAT', 'FORD', 'HINDUSTAN MOTORS (HM)', 'HONDA', 'HUMMER', 'HYUNDAI', 'JAGUAR', 'LAMBORGHINI', 'LAND ROVER GROUP', 'MAHINDRA', 'MARUTI', 'MAYBACH', 'MERCEDES-BENZ', 'MINI (BMW)', 'MITSUBISHI', 'NISSAN', 'OPEL', 'PEUGEOT', 'PIAGGIO', 'PORSCHE', 'PREMIER', 'RENAULT', 'ROLLS-ROYCE', 'SCOOTERS INDIA LIMITED', 'SKODA', 'SUZUKI', 'TATA (TELCO)', 'TOYOTA', 'TVS', 'VOLVO', 'VW (VOLKSWAGEN)']
fw1 = open('links_v.txt','w')
fw2 = open('links_e.txt','w')

for m in makes :
	m = m.strip()
	browser = webdriver.Chrome()
	browser.set_window_size(1366,768)
	url = 'http://www.bosch-automotive-catalog.com/en/?country=IN'
	browser.get(url)
	
	el1 = browser.find_element_by_id('idMake')
	options = el1.find_elements_by_tag_name('option')

	for i in options :
		if i.text == m :
			i.click()

			time.sleep(3)
			el2 = browser.find_element_by_id('idModelRange')
			options_mdl = el2.find_elements_by_tag_name('option')
			
			for j in options_mdl:

				try :				
					if str(j.text)[0] != '.' :
						print j.text,"\n"
						j.click()
				
						time.sleep(3)
						browser.find_element_by_id('VehicleSearchSubmit').click()
						
						time.sleep(3)
						tds = browser.find_elements_by_class_name('actions')
						for td in tds :
							li = td.find_elements_by_tag_name('a')
							for i in li :
								link = i.get_attribute('href')
								
								if link.split('/')[-4].lower() == 'equip' :
									w = m + " : " + j.text + " : " + " passenger : petrol " + link
									fw2.write(w+'\n')
									print w
								else :
									w = m + " : " + j.text + " : " + " passenger : petrol " + link
									fw1.write(w+'\n')
									print w
						os.system("xdotool mousemove 1300 250 click 1")
				except :
					os.system("xdotool mousemove 1300 250 click 1")

	browser.close()				