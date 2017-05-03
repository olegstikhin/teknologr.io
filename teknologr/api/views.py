from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from api.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from members.models import GroupMembership, Member, Group


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


# User accounts

@api_view(['POST'])
def create_accounts(request):
    '''Create LDAP and BILL accounts for given user'''
    from api.ldap import LDAPAccountManager
    member_id = request.data.get('member_id')
    member = get_object_or_404(Member, id=member_id)
    username = request.data.get('username')
    password = request.data.get('password')
    error = None
    with LDAPAccountManager() as lm:
        error = lm.add_account(member, username, password)

    if error:
        return Response({"LDAP": error}, status=400)

    # TODO create BILL account
    bill_code = None

    # Store account details
    member.username = username
    member.bill_code = bill_code
    member.save()

    return Response(status=200)


@api_view(['POST'])
def delete_accounts(request):
    from api.ldap import LDAPAccountManager
    member_id = request.data.get('member_id')
    member = get_object_or_404(Member, id=member_id)

    with LDAPAccountManager() as lm:
        error = lm.delete_account(member.username)

    # TODO: delete BILL account
    member.username = None
    member.bill_code = None
    member.save()

    if error:
        return Response(error, status=400)
    return Response(status=200)


@api_view(['POST'])
def change_password(request):
    from api.ldap import LDAPAccountManager
    member_id = request.data.get('member_id')
    member = get_object_or_404(Member, id=member_id)
    password = request.data.get('password')

    with LDAPAccountManager() as lm:
        error = lm.change_password(member.username, password)

    if error:
        return Response(error, status=400)
    return Response(status=200)
