from django.shortcuts import render
from rest_framework import viewsets
from api.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils import *
import json

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

    gid = request.data.get('group')
    members = request.data.get('member').strip("|").split("|")

    for mid in members:
        # get_or_create is used to ignore duplicates
        GroupMembership.objects.get_or_create(member_id=int(mid), group_id=int(gid))

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

# JSON API:s

@api_view(['GET'])
def memberTypesForMember(request, query):

    member = findMembers(query, 1).first()

    if not member:
        return Response(status=404)


    membertypes = []

    for e in MemberType.objects.filter(member=member):
        membertypes.append((e.type, str(e.begin_date), str(e.end_date)))
    data = json.dumps({
        "given_names": member.given_names.split(),
        "surname": member.surname,
        "nickname": member.nickname,
        "preferred_name": member.preferred_name,
        "membertypes": membertypes
        }
    )

    return Response(data,status=200)