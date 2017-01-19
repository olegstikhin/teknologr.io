from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/members/')),
    url(r'^(members|groups|functionaries|decorations)/$', views.empty),
    url(r'^members/(\d+)/$', views.member),
    url(r'^members/new/$', views.new_member),
    url(r'^members/(\d+)/del', views.delete_member),
    url(r'^groups/(\d+)/$', views.group),
    url(r'^groups/new/$', views.new_group),
    url(r'^groups/(\d+)/del', views.delete_grouptype),
    url(r'^functionaries/(\d+)/$', views.functionary),
    url(r'^decorations/(\d+)/$', views.decoration),

]