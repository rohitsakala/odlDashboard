''' The functions in the file are written to call API's and store the response in the database '''

import requests
import csv
import re
from datetime import date
from datetime import timedelta
from celery.utils.log import get_task_logger
from scripts.models import Projects,Bugs,Test,Commit,Contributors

logger = get_task_logger(__name__)


''' Function related to populating list of opendaylight projects '''

# From Bugzilla
def getProjectsList():
	url = "https://bugs.opendaylight.org/report.cgi?resolution=---&y_axis_field=product&width=1024&height=600&action=wrap&ctype=csv&format=table"
	method = "GET"
	r = requests.get(url)
	reader = csv.reader(r.text.split('\n'), delimiter=',')
	for count,row in enumerate(reader):
		if count != 0:
			Projects.objects.update_or_create(name=row[0])

# From Github
def getRepos():
	page = 1
	while 1:
		url = "https://api.github.com/orgs/opendaylight/repos?page="+str(page)+"&per_page=100"
		r = requests.get(url, auth=('rohitsakala', 'Radha.sakala8'))
		for i in range(len(r.json())):
			name = r.json()[i]['name']
			try:
				project = Projects.objects.get(name=name)
			except:
				Projects.objects.update_or_create(name=name)
		if r.links:
			try:
				page = r.links['next']['url'].split("=")[1].split("&")[0]
			except:
				break
		else:
			break

# From Sonar
def getComponents():
	url = "https://sonar.opendaylight.org/api/resources?format=json"
	method = "GET"
	r = requests.get(url)
	for i in range(len(r.json())):
		if 'branch'  not in r.json()[i]:
			name = re.split(':',r.json()[i]['key'])
			m = re.search('org.opendaylight.(.*)',name[0])
			try:
				project = Projects.objects.get(name=m.group(1))
			except:
				if m.group(1) != "ofconfig" and m.group(1) != "ofextensions.circuitsw":
					Projects.objects.update_or_create(name=m.group(1))
					
''' Function related to populating values of attributes of BugZilla '''

# Bug Status
def getBugStatus():
	url = "https://bugs.opendaylight.org/report.cgi?resolution=---&x_axis_field=bug_status&y_axis_field=product&width=1024&height=600&action=wrap&ctype=csv&format=table"
	method = "GET"
	r = requests.get(url)
	reader = csv.reader(r.text.split('\n'), delimiter=',')
	for count,row in enumerate(reader):
		if count != 0:
			project = Projects.objects.get(name=row[0])		
			Bugs.objects.update_or_create(projectName=project,defaults={'unconfirmed':row[1],'confirmed':row[2],'inProgress':row[3],'waitingForReview':row[4]})


# Bug Severity
def getBugSeverity():
	url = "https://bugs.opendaylight.org/report.cgi?resolution=---&x_axis_field=bug_severity&y_axis_field=product&width=1024&height=600&action=wrap&ctype=csv&format=table"
	method = "GET"
	r = requests.get(url)
	reader = csv.reader(r.text.split('\n'), delimiter=',')
	for count,row in enumerate(reader):
		if count != 0:
			project = Projects.objects.get(name=row[0])
			Bugs.objects.update_or_create(projectName=project,defaults={'blocker':row[1],'critical' : row[2],'major' : row[3],'normal' : row[4],'minor' : row[5],'trivial' : row[6],'enhancement' : row[7]})

# Bug Priority
def getBugPriority():
	url = "https://bugs.opendaylight.org/report.cgi?resolution=---&x_axis_field=priority&y_axis_field=product&width=1024&height=600&action=wrap&ctype=csv&format=table"
	method = "GET"
	r = requests.get(url)
	reader = csv.reader(r.text.split('\n'), delimiter=',')
	for count,row in enumerate(reader):
		if count != 0:
			project = Projects.objects.get(name=row[0])
			Bugs.objects.update_or_create(projectName=project,defaults={'highest':row[1],'high' : row[2],'normal' : row[3],'low' : row[4],'lowest' : row[5]})

''' Function related to populating values of attributes of Sonar '''

# Test Coverage
def getTestCoverage():
	url = "https://sonar.opendaylight.org/api/resources?metrics=coverage&format=json"
	method = "GET"
	r = requests.get(url)
	for i in range(len(r.json())):
		if 'branch'  not in r.json()[i]:
			name = re.split(':',r.json()[i]['key'])
			m = re.search('org.opendaylight.(.*)',name[0])
			if m.group(1) == "ofconfig":
				project = Projects.objects.get(name="of-config")
			elif m.group(1) == "ofextensions.circuitsw":
				project = Projects.objects.get(name="ofextensions-circuitsw")
			else:
				project = Projects.objects.get(name=m.group(1))
			Test.objects.update_or_create(projectName=project,defaults={'coverage':r.json()[i]['msr'][0]['val']})

# Test Success Density
def getSuccessDensity():
	url = "https://sonar.opendaylight.org/api/resources?metrics=test_success_density&format=json"
	r = requests.get(url)
	for i in range(len(r.json())):
		if 'branch'  not in r.json()[i]:
			name = re.split(':',r.json()[i]['key'])
			m = re.search('org.opendaylight.(.*)',name[0])
			if m.group(1) == "ofconfig":
				project = Projects.objects.get(name="of-config")
			elif m.group(1) == "ofextensions.circuitsw":
				project = Projects.objects.get(name="ofextensions-circuitsw")
			else:
				project = Projects.objects.get(name=m.group(1))
			Test.objects.update_or_create(projectName=project,defaults={'successDensity':r.json()[i]['msr'][0]['val']})

''' Function related to populating values of attributes of Github '''

# Total number of Commits
def getCommitCountTotal():
	projects = Projects.objects.all()
	for project in projects:
		page = 1
		count = 0
		while 1:
			url = "https://api.github.com/repos/opendaylight/"+project.name+"/commits?page="+str(page)+"&per_page=100"
			r = requests.get(url, auth=('rohitsakala', 'Radha.sakala8'))
			if r.status_code == 200:
				count = count + len(r.json())
				if r.links:
					try:
						page = r.links['next']['url'].split("=")[1].split("&")[0]
					except:
						Commit.objects.update_or_create(projectName=project,defaults={'totalCount':count})
						break
				else:
					Commit.objects.update_or_create(projectName=project,defaults={'totalCount':count})
					break
			else:
				break

# Total number of commits last week
def getCommitCountLastWeek():
	projects = Projects.objects.all()
	today = date.today()
	lastDate = today - timedelta(days=7)
	for project in projects:
		page = 1
		count = 0
		while 1:
			url = "https://api.github.com/repos/opendaylight/"+project.name+"/commits?page="+str(page)+"&per_page=100&since="+str(lastDate)
			r = requests.get(url, auth=('rohitsakala', 'Radha.sakala8'))
			if r.status_code == 200:
				count = count + len(r.json())
				if r.links:
					try:
						page = r.links['next']['url'].split("=")[1].split("&")[0]
					except:
						Commit.objects.update_or_create(projectName=project,defaults={'lastWeekCount':count})
						break
				else:
					Commit.objects.update_or_create(projectName=project,defaults={'lastWeekCount':count})
					break
			else:
				break

# List of contributors and their count
def getContributorsCount():
	projects = Projects.objects.all()
	for project in projects:
		page = 1
		while 1:
			url = "https://api.github.com/repos/opendaylight/"+project.name+"/contributors?page="+str(page)+"&per_page=100"
			r = requests.get(url, auth=('rohitsakala', 'Radha.sakala8'))
			if r.status_code == 200:
				for i in range(len(r.json())):
					name = r.json()[i]["login"]
					count = r.json()[i]["contributions"]
					Contributors.objects.update_or_create(projectName=project,contributorName=name,defaults={'contributionCount':count})
				if r.links:
					try:
						page = r.links['next']['url'].split("=")[1].split("&")[0]
					except:
						break
				else:
					break
			else:
				break