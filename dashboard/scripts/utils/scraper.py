''' The functions in the file are written to call API's and store the response in the database '''

import requests
import csv
from celery.utils.log import get_task_logger
from scripts.models import Projects,Bugs

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
			project = Projects.objects.get(name=row[0])
			#Bugs.objects.update_or_create(projectName=project,unconfirmed=row[1],confirmed=row[2],inProgress=row[3],waitingForReview=row[4])
			Bugs.objects.update_or_create(projectName=project,defaults={'unconfirmed':row[1],'confirmed':row[2],'inProgress':row[3],'waitingForReview':row[4]})

def getBugSeverity():
	url = "https://bugs.opendaylight.org/report.cgi?resolution=---&x_axis_field=bug_severity&y_axis_field=product&width=1024&height=600&action=wrap&ctype=csv&format=table"
	method = "GET"
	r = requests.get(url)
	reader = csv.reader(r.text.split('\n'), delimiter=',')
	for count,row in enumerate(reader):
		if count != 0:
			project = Projects.objects.get(name=row[0])
			Bugs.objects.update_or_create(projectName=project,defaults={'blocker':row[1],'critical' : row[2],'major' : row[3],'normal' : row[4],'minor' : row[5],'trivial' : row[6],'enhancement' : row[7]})

def getBugPriority():
	url = "https://bugs.opendaylight.org/report.cgi?resolution=---&x_axis_field=priority&y_axis_field=product&width=1024&height=600&action=wrap&ctype=csv&format=table"
	method = "GET"
	r = requests.get(url)
	reader = csv.reader(r.text.split('\n'), delimiter=',')
	for count,row in enumerate(reader):
		if count != 0:
			project = Projects.objects.get(name=row[0])
			Bugs.objects.update_or_create(projectName=project,defaults={'highest':row[1],'high' : row[2],'normal' : row[3],'low' : row[4],'lowest' : row[5]})
