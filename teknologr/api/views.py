from django.shortcuts import render
from rest_framework import viewsets
from api.serializers import *

# Create your views here.

# ViewSets define the view behavior.

# Members

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


# Groups

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupTypeViewSet(viewsets.ModelViewSet):
    queryset = GroupType.objects.all()
    serializer_class = GroupTypeSerializer

class GroupMembershipViewSet(viewsets.ModelViewSet):
    queryset = GroupMembership.objects.all()
    serializer_class = GroupMembershipSerializer


# Functionaries

class FunctionaryViewSet(viewsets.ModelViewSet):
    queryset = Functionary.objects.all()
    serializer_class = FunctionarySerializer

class FunctionaryTypeViewSet(viewsets.ModelViewSet):
    queryset = FunctionaryType.objects.all()
    serializer_class = FunctionaryTypeSerializer


# Decorations

class DecorationViewSet(viewsets.ModelViewSet):
    queryset = Decoration.objects.all()
    serializer_class = DecorationSerializer

class DecorationOwnershipViewSet(viewsets.ModelViewSet):
    queryset = DecorationOwnership.objects.all()
    serializer_class = DecorationOwnershipSerializer


# MemberTypes

class MemberTypeViewSet(viewsets.ModelViewSet):
    queryset = MemberType.objects.all()
    serializer_class = MemberTypeSerializer