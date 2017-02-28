from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/members/')),
    url(r'^(members|groups|functionaries|decorations)/$', views.empty),
    url(r'^members/(\d+)/$', views.member),
    url(r'^members/new/$', views.new_member),
    url(r'^groups/(\d+)/$', views.group),
    url(r'^groups/(\d+)/(\d+)/$', views.group),
    url(r'^groups/new/$', views.new_group),
    url(r'^functionaries/(\d+)/$', views.functionary),
    url(r'^functionaries/new/$', views.new_functionarytype),
    url(r'^decorations/(\d+)/$', views.decoration),
    url(r'^decorations/new/$', views.new_decoration),
]