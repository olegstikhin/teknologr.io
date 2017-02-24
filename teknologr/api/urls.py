from django.conf.urls import url, include
from rest_framework import routers
from api.views import *

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'groupTypes', GroupTypeViewSet)
router.register(r'groupMembership', GroupMembershipViewSet)
router.register(r'functionaries', FunctionaryViewSet)
router.register(r'functionaryTypes', FunctionaryTypeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
