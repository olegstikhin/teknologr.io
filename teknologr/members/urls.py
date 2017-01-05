from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$|^home/$', views.home_view),
]