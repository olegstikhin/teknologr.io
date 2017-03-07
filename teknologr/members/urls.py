from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/members/')),
    url(r'^(members|groups|functionaries|decorations)/$', views.empty),
    url(r'^members/(\d+)/$', views.member),
    url(r'^groups/(\d+)/$', views.group),
    url(r'^groups/(\d+)/edit$', views.editgroup),
    url(r'^groups/(\d+)/(\d+)/$', views.group),
    url(r'^functionaries/(\d+)/$', views.functionary),
    url(r'^decorations/(\d+)/$', views.decoration),
]