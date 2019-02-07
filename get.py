#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from string import ascii_lowercase
from csv import writer  


#gender of the child
gender=["boy","girl"]

#base url of the site to be scrap
baseUrl="https://www.babynamesdirect.com";

#response for the request form the basr url
response=requests.get(baseUrl);

#html parser for the url soup=>object for the bs4 BeautifulSoup
soup=BeautifulSoup(response.text,'html.parser')

#loocking for the specific details
options=soup.find_all('option')

typeName=[]

#filtering data
for option in options:
	category=option.get_text();
	if(category!='Category' and category!='Contains' and category!='Starting from' and category!='Ends with'):
		str1=option.get_text();
		str1=str1.replace('⋅ ', '')
		typeName.append(str1.lower());

#print(typeName);
typeName=typeName[:len(typeName)//2]
				
# new url for crawler
nameUrl=baseUrl+"/baby-names";


urls=[];
finalUrl=[];
hrf=[]

#creating distinct url for to scrapp full site 
for typ in typeName:
		for c in ascii_lowercase:
			actualUrlboy=nameUrl+'/'+typ+'/'+gender[0]+'/'+c;
			actualUrlgirl=nameUrl+'/'+typ+'/'+gender[1]+'/'+c;
			urls.append(actualUrlboy);
			urls.append(actualUrlgirl);
			

def scrapper(url):
		hrf.append(url)
		response=requests.get(url);
		soup=BeautifulSoup(response.text,'html.parser')
		data=soup.find_all(class_='nvar')
		crawler=soup.find("nav",attrs={"class":"pages"})
		headder=["Name"]

		fName=url.lower().split('/')
		print(url);
		with open(fName[4]+'.csv','a') as csv_file:
			csv_writer=writer(csv_file)
			csv_writer.writerow(headder)

			for d in data:
				name=d.get_text();
				if(name != 'Name'):
					csv_writer.writerow([name])	
					
			if(crawler):
				for a in crawler:
					href=a.get('href')
					if(href):
						if(href not in hrf):
							hrf.append(href)
							scrapper(href);


for url in urls:
	scrapper(url);
	# break;
