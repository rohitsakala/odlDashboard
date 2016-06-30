from django.conf.urls import url

from . import views

urlpatterns = [
	# /main/
    url(r'^$', views.index, name='index'),
    # /main/projects/id
    url(r'^project/(?P<project_id>[0-9]+)/$', views.project, name='project'),
    # /main/performance
    url(r'^performance/(?P<component>.*)/$', views.performance, name='performance'),
    # /main/comparison
    url(r'^comparison/', views.comparison, name='comparison'),
]
