from django.contrib import admin
from .models import Projects,Bugs,Urls,PerformanceGraphs

admin.site.register(Projects)
admin.site.register(Bugs)
admin.site.register(Urls)
admin.site.register(PerformanceGraphs)
