from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


urlpatterns = [
    url(r'^status/?(?P<channel_name>\w+)?', views.status, name='status'),
    url(r'^fundalogin/', views.funda_login, name='fundalogin'),
]

urlpatterns += staticfiles_urlpatterns()