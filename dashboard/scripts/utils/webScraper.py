''' The functions in the file are written to call API's and store the response in the database '''

import requests
import csv
import re
from datetime import date
from datetime import timedelta
from celery.utils.log import get_task_logger
from bs4 import BeautifulSoup
from scripts.models import Urls,PerformanceGraphs

logger = get_task_logger(__name__)

def getPerformanceGraphs():
	urls = Urls.objects.all()
	for url in urls:
		r = requests.get(url.url)
		soup = BeautifulSoup(r.text,'html.parser')
		mainUrl = url
		componentName = ""
		for i in soup.find_all('h3'):
			componentName = i.string
			toolUsed = i.find_next('h4').string
			ul = i.find_next('ul')
			for li in ul.find_all('li'):
				jenkinsUrl = li.find_next('a').get('href')
				jobName = li.find_next('a').string
				r2 = requests.get(jenkinsUrl)
				soup2 = BeautifulSoup(r2.text,'html.parser')
				for i in range(len(soup2.find('select').find_all('option'))):
					newUrl = jenkinsUrl + "getPlot?index="+str(i)+"&width=750&height=450"
					plotId = i
					PerformanceGraphs.objects.update_or_create(mainUrl=url,jobName=jobName,toolUsed=toolUsed,componentName=componentName,jenkinsUrl=newUrl,plotId=plotId)






