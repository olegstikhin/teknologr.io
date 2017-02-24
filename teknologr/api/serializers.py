from django_countries import Countries
from rest_framework import serializers
from members.models import *


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