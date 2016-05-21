''' The functions in the file are written to call API's and store the response in the database '''

import requests
import csv
import re
from celery.utils.log import get_task_logger
from scripts.models import Projects,Bugs,Test

logger = get_task_logger(__name__)


''' Functions related to Bugzilla API '''

def getProjectsList():
	url = "https://bugs.opendaylight.org/report.cgi?resolution=---&y_axis_field=product&width=1024&height=600&action=wrap&ctype=csv&format=table"
	method = "GET"
	r = requests.get(url)
	reader = csv.reader(r.text.split('\n'), delimiter=',')
	for count,row in enumerate(reader):
		if count != 0:
			Projects.objects.update_or_create(name=row[0])

def getBugStatus():
	url = "https://bugs.opendaylight.org/report.cgi?resolution=---&x_axis_field=bug_status&y_axis_field=product&width=1024&height=600&action=wrap&ctype=csv&format=table"
	method = "GET"
	r = requests.get(url)
	reader = csv.reader(r.text.split('\n'), delimiter=',')
	for count,row in enumerate(reader):
		if count != 0:
			try:
				project = Projects.objects.get(name=row[0])
			except:
				Projects.objects.update_or_create(name=row[0])
				project = Projects.objects.get(name=row[0])		
			Bugs.objects.update_or_create(projectName=project,defaults={'unconfirmed':row[1],'confirmed':row[2],'inProgress':row[3],'waitingForReview':row[4]})

def getBugSeverity():
	url = "https://bugs.opendaylight.org/report.cgi?resolution=---&x_axis_field=bug_severity&y_axis_field=product&width=1024&height=600&action=wrap&ctype=csv&format=table"
	method = "GET"
	r = requests.get(url)
	reader = csv.reader(r.text.split('\n'), delimiter=',')
	for count,row in enumerate(reader):
		if count != 0:
			try:
				project = Projects.objects.get(name=row[0])
			except:
				Projects.objects.update_or_create(name=row[0])
				project = Projects.objects.get(name=row[0])
			Bugs.objects.update_or_create(projectName=project,defaults={'blocker':row[1],'critical' : row[2],'major' : row[3],'normal' : row[4],'minor' : row[5],'trivial' : row[6],'enhancement' : row[7]})

def getBugPriority():
	url = "https://bugs.opendaylight.org/report.cgi?resolution=---&x_axis_field=priority&y_axis_field=product&width=1024&height=600&action=wrap&ctype=csv&format=table"
	method = "GET"
	r = requests.get(url)
	reader = csv.reader(r.text.split('\n'), delimiter=',')
	for count,row in enumerate(reader):
		if count != 0:
			try:
				project = Projects.objects.get(name=row[0])
			except:
				Projects.objects.update_or_create(name=row[0])
				project = Projects.objects.get(name=row[0])
			Bugs.objects.update_or_create(projectName=project,defaults={'highest':row[1],'high' : row[2],'normal' : row[3],'low' : row[4],'lowest' : row[5]})

def getTestCoverage():
	url = "https://sonar.opendaylight.org/api/resources?metrics=coverage&format=json"
	method = "GET"
	r = requests.get(url)
	for i in range(len(r.json())):
		if 'branch'  not in r.json()[i]:
			name = re.split(':',r.json()[i]['key'])
			m = re.search('org.opendaylight.(.*)',name[0])
			try:
				project = Projects.objects.get(name=m.group(1))
			except:
				Projects.objects.update_or_create(name=m.group(1))
				project = Projects.objects.get(name=m.group(1))
			Test.objects.update_or_create(projectName=project,defaults={'coverage':r.json()[i]['msr'][0]['val']})

def getSuccessDensity():
	url = "https://sonar.opendaylight.org/api/resources?metrics=test_success_density&format=json"
	method = "GET"
	r = requests.get(url)
	for i in range(len(r.json())):
		if 'branch'  not in r.json()[i]:
			name = re.split(':',r.json()[i]['key'])
			m = re.search('org.opendaylight.(.*)',name[0])
			try:
				project = Projects.objects.get(name=m.group(1))
			except:
				Projects.objects.update_or_create(name=m.group(1))
				project = Projects.objects.get(name=m.group(1))
			Test.objects.update_or_create(projectName=project,defaults={'successDensity':r.json()[i]['msr'][0]['val']})

			
