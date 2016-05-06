f = open('links_e.txt')

li = []
for i in f :
	j = i.strip().replace(" passenger : petrol ","").split(" : ")
	w = j[0]+","+j[1].split("  ")[0].strip()+","+j[-1]
	li.append(w)

print len(li)
k = list(set(li))
print len(k)

fw = open('petrol_passenger_links.txt','w')
for i in k:
	fw.write(i.strip()+'\n')

