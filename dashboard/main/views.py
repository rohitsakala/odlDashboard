from django.shortcuts import get_object_or_404,HttpResponse,render
from scripts.models import Projects,Bugs,Test,Commit,Contributors,PerformanceGraphs

def index(request):
    projectList = Projects.objects.all()
    components = PerformanceGraphs.objects.order_by().values('componentName').distinct()
    data = {'projectList' : projectList,'components':components}
    return render(request, 'main/projectList.html', data)

def project(request, project_id):
    project = get_object_or_404(Projects, pk=project_id)
    components = PerformanceGraphs.objects.order_by().values('componentName').distinct()
    try:
        bugs = Bugs.objects.get(projectName=project)
    except:
        bugs = None
    try:
        test = Test.objects.get(projectName=project)
    except:
        test = None
    try:
        commit = Commit.objects.get(projectName=project)
    except:
        commit = None
    try:
        contributors = Contributors.objects.filter(projectName=project)
    except:
        contributors = None
    data = {'project' : project,'bugs' : bugs,'test' : test,'commit' : commit,'contributors' : contributors,'components':components}
    return render(request, 'main/project.html', data)

def performance(request,name):
    performanceGraphs = PerformanceGraphs.objects.filter(componentName=name)
    components = PerformanceGraphs.objects.order_by().values('componentName').distinct()
    data = {'performance' : performanceGraphs,'name':name,'components':components}
    return render(request, 'main/performance.html', data)