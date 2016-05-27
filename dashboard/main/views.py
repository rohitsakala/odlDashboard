from django.shortcuts import get_object_or_404,HttpResponse,render
from scripts.models import Projects,Bugs,Test,Commit

def index(request):
	projectList =  Projects.objects.all()
	data = {'projectList' : projectList}
    	return render(request, 'main/projectList.html', data)

def project(request, project_id):
    project = get_object_or_404(Projects, pk=project_id)
    bugs = get_object_or_404(Bugs,projectName=project)
    test = get_object_or_404(Test,projectName=project)
    commit = get_object_or_404(Commit,projectName=project)
    data = {'project' : project,'bugs' : bugs,'test' : test,'commit' : commit}
    return render(request, 'main/project.html', data)
