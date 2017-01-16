from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/members/')),
    url(r'^(members|groups|functionaries|decorations)/$', views.empty),
    url(r'^members/(\d+|new)$', views.member),
    url(r'^groups/(\w+)$', views.group),
    url(r'^functionaries/(\w+)$', views.functionary),
    url(r'^decorations/(\w+)$', views.decoration),

]