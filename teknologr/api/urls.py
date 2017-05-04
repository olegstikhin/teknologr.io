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
router.register(r'decorations', DecorationViewSet)
router.register(r'decorationOwnership', DecorationOwnershipViewSet)
router.register(r'memberTypes', MemberTypeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^multiGroupMembership/$', memberListSave),
    url(r'^memberTypesForMember/(?P<mode>username|studynumber)/(?P<query>[A-Za-z0-9]+)/$', memberTypesForMember),
    url(r'^accounts/ldap/add$', create_ldap_account),
    url(r'^accounts/ldap/delete$', delete_ldap_account),
    url(r'^accounts/ldap/change_pw$', change_ldap_password),
    url(r'^accounts/ldap/info/(\d+)/$', get_ldap_info),
    url(r'^accounts/bill/add$', create_bill_account),
    url(r'^accounts/bill/delete$', delete_bill_account),
    url(r'^accounts/bill/info/(\d+)/$', get_bill_info),
]
