from django.conf.urls import url, include
from django.contrib.auth.models import User
from django_countries import Countries
from members.models import Member, Group, GroupType, GroupMembership, Functionary, FunctionaryType
from rest_framework import routers, serializers, viewsets


class SerializableCountryField(serializers.ChoiceField):
    def to_representation(self, value):
        if value in ('', None):
            return ''  # instead of `value` as Country(u'') is not serializable
        return super(SerializableCountryField, self).to_representation(value)

# Serializers define the API representation.
class MemberSerializer(serializers.HyperlinkedModelSerializer):
    country = SerializableCountryField(allow_blank=True, choices=Countries())
    class Meta:
        model = Member
        fields = ('full_name', 'full_preferred_name', 'given_names', 'preferred_name', 'surname', 'maiden_name',\
            'nickname', 'birth_date', 'student_id', 'gender', 'graduated', 'graduated_year', 'dead', 'mobile_phone', \
            'phone', 'street_address', 'postal_code', 'city', 'country', 'url', 'email', 'subscribed_to_modulen', \
            'allow_publish_info', 'username', 'crm_id')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group

class GroupTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GroupType

class GroupMembershipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GroupMembership

class FunctionarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Functionary

class FunctionaryTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FunctionaryType



# ViewSets define the view behavior.
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupTypeViewSet(viewsets.ModelViewSet):
    queryset = GroupType.objects.all()
    serializer_class = GroupTypeSerializer

class GroupMembershipViewSet(viewsets.ModelViewSet):
    queryset = GroupMembership.objects.all()
    serializer_class = GroupMembershipSerializer

class FunctionaryViewSet(viewsets.ModelViewSet):
    queryset = Functionary.objects.all()
    serializer_class = FunctionarySerializer

class FunctionaryTypeViewSet(viewsets.ModelViewSet):
    queryset = FunctionaryType.objects.all()
    serializer_class = FunctionaryTypeSerializer

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
