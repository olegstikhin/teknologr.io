from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$|^home/$', views.home_view),
    url(r'^side/(members|groups|functionaries|decorations)$', views.side),
    url(r'^members/(\w+)$', views.member),
    url(r'^groups/(\w+)$', views.group),
    url(r'^functionaries/(\w+)$', views.functionary),
    url(r'^decorations/(\w+)$', views.decoration),

]