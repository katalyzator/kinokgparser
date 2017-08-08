from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from kinokgparser import settings
from parse_app.views import parse, main, get_json

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api/v1/cinema/$', main, name='parse'),
    url(r'get/$', get_json, name='some')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)