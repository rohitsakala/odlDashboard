''' The functions in the file are written to call API's and store the response in the database '''

import requests
import csv
from celery.utils.log import get_task_logger
from scripts.models import Projects

logger = get_task_logger(__name__)

def getProjectsList():
	url = "https://bugs.opendaylight.org/report.cgi?resolution=---&y_axis_field=product&width=1024&height=600&action=wrap&ctype=csv&format=table"
	method = "GET"
	r = requests.get(url)
	reader = csv.reader(r.text.split('\n'), delimiter=',')
	for count,row in enumerate(reader):
		if count != 0:
			Projects.objects.get_or_create(name=row[0])
