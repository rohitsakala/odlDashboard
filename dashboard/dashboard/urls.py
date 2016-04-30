from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^main/', include('main.urls')),
    url(r'^scripts/', include('scripts.urls')),
]
