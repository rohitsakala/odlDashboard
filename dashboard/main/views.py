from django.shortcuts import HttpResponse
from scripts.models import Projects

def index(request):
	projectList =  Projects.objects.all()
    	return HttpResponse(projectList)