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
		for i in soup.find_all('h2'):
			s = i.find_next(class_="mw-headline").string
			plugin = s[s.find("(")+1:s.find(")")]
			seen = set()
			for y in i.find_next_siblings('h3'):
				componentName = y.string
				if componentName in seen:
					pass
				else:
					seen.add(componentName)
					toolUsed = y.find_next('h4').string
					ul = y.find_next('ul')
					for li in ul.find_all('li'):
						jenkinsUrl = li.find_next('a').get('href')
						jobName = li.find_next('a').string
						r2 = requests.get(jenkinsUrl)
						soup2 = BeautifulSoup(r2.text,'html.parser')
						length = 0
						try:
							length = len(soup2.find('select').find_all('option'))
						except:
							pass
						if length != 0:
							for x in range(length):
								newUrl = jenkinsUrl + "getPlot?index="+str(x)+"&width=750&height=450"
								m=re.search(".*/job/(.*)/plot.*",newUrl)
								jenkinsJobName = m.group(1)
								plotId = x
								PerformanceGraphs.objects.update_or_create(plugin=plugin,plotId=plotId,jobName=jobName,defaults={'jenkinsJobName':jenkinsJobName,'mainUrl':url,'toolUsed':toolUsed,'componentName':componentName,'jenkinsUrl':newUrl})
