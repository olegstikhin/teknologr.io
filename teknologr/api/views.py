from django.shortcuts import render
from rest_framework import viewsets
from api.serializers import *
from rest_framework.decorators import api_view

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

@api_view(['POST'])
def memberListSave(request):
    from members.models import GroupMembership, Member, Group
    from rest_framework.response import Response
    
    # [0] is key, [1] is values
    gid = request.data.get('group')
    members = request.data.get('member').strip("|").split("|")

    for mid in members:
        member = Member.objects.get(pk=int(mid))
        group = Group.objects.get(pk=int(gid))
        GroupMembership.objects.create(member = member,group = group)

    return Response(status=200)

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
