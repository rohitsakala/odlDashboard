from django.shortcuts import get_object_or_404,HttpResponse,render
from scripts.models import Projects,Bugs,Test,Commit,Contributors,PerformanceGraphs
import json

def index(request):
    projectList = Projects.objects.all()
    plugins = PerformanceGraphs.objects.values('plugin').distinct()
    pluginComponent = {}
    for i in range(len(plugins)):
        pluginComponent[plugins[i]['plugin']] = PerformanceGraphs.objects.filter(plugin=plugins[i]['plugin']).order_by().values('componentName').distinct()
    data = {'projectList' : projectList,'pluginComponent':pluginComponent}
    return render(request, 'main/list.html', data)

def project(request, project_id):
    project = get_object_or_404(Projects, pk=project_id)
    plugins = PerformanceGraphs.objects.values('plugin').distinct()
    pluginComponent = {}
    for i in range(len(plugins)):
        pluginComponent[plugins[i]['plugin']] = PerformanceGraphs.objects.filter(plugin=plugins[i]['plugin']).order_by().values('componentName').distinct()
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
    data = {'project' : project,'bugs' : bugs,'test' : test,'commit' : commit,'contributors' : contributors,'pluginComponent':pluginComponent}
    return render(request, 'main/project.html', data)

def performance(request,name,plugin):
    performanceGraphs = PerformanceGraphs.objects.filter(componentName=name,plugin=plugin)
    plugins = PerformanceGraphs.objects.values('plugin').distinct()
    pluginComponent = {}
    for i in range(len(plugins)):
        pluginComponent[plugins[i]['plugin']] = PerformanceGraphs.objects.filter(plugin=plugins[i]['plugin']).order_by().values('componentName').distinct()
    data = {'performance' : performanceGraphs,'name':name,'pluginComponent':pluginComponent}
    return render(request, 'main/performance.html', data)

def comparison(request):
    bugs = Bugs.objects.all()
    projects = []
    values = []
    for bug in bugs:
        projects.append(str(bug.projectName.name))
        values.append(bug.major + bug.minor + bug.normal + bug.highest + bug.high + bug.critical + bug.blocker)
    data = {'projects' : projects,'values' : values}
    return render(request, 'main/comparison.html', data) 
