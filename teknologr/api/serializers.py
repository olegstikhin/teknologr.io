from django_countries import Countries
from rest_framework import serializers
from members.models import *


class SerializableCountryField(serializers.ChoiceField):
    def to_representation(self, value):
        if value in ('', None):
            return ''  # instead of `value` as Country(u'') is not serializable
        return super(SerializableCountryField, self).to_representation(value)

# Serializers define the API representation.

# Members

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    country = SerializableCountryField(allow_blank=True, choices=Countries())
    class Meta:
        model = Member
        fields = '__all__'


# Groups

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class GroupTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GroupType
        fields = '__all__'

class GroupMembershipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GroupMembership
        fields = '__all__'


# Functionaries

class FunctionarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Functionary
        fields = '__all__'

class FunctionaryTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FunctionaryType
        fields = '__all__'


# Decorations

class DecorationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Decoration
        fields = '__all__'

class DecorationOwnershipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DecorationOwnership
        fields = '__all__'
