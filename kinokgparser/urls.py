from django.conf.urls import url
from django.contrib import admin

from parse_app.views import parse, main

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api/v1/cinema/$', main, name='parse')
]
