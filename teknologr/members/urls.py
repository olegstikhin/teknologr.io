from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from members.forms import BSAuthForm
from . import views
from ajax_select import urls as ajax_select_urls


urlpatterns = [
	url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form':BSAuthForm}),
	url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}),
    url(r'^$', RedirectView.as_view(url='/members/')),
    url(r'^(members|groups|functionaries|decorations)/$', views.empty),
    url(r'^members/(\d+)/$', views.member),
    url(r'^membertype/(\d+)/form/', views.membertype_form),
    url(r'^groups/(\d+)/$', views.group),
    url(r'^groups/(\d+)/(\d+)/$', views.group),
    url(r'^functionaries/(\d+)/$', views.functionary),
    url(r'^decorations/(\d+)/$', views.decoration),
    url(r'^ajax_select/', include(ajax_select_urls)),
]