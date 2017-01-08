from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$|^home/$', views.home_view),
    url(r'^$|^side_members/$', views.side_members),
    url(r'^$|^member/(\w+)$', views.member),
]