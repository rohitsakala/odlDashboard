from django.shortcuts import get_object_or_404,HttpResponse,render
from scripts.models import Projects,Bugs,Test,Commit,Contributors

def index(request):
	projectList =  Projects.objects.all()
	data = {'projectList' : projectList}
    	return render(request, 'main/projectList.html', data)

def project(request, project_id):
    project = get_object_or_404(Projects, pk=project_id)
    bugs = Bugs.objects.get(projectName=project)
    test = Test.objects.get(projectName=project)
    commit = Commit.objects.get(projectName=project)
    contributors = Contributors.objects.filter(projectName=project)
    data = {'project' : project,'bugs' : bugs,'test' : test,'commit' : commit,'contributors' : contributors}
    return render(request, 'main/project.html', data)
