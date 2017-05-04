from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from api.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from members.models import GroupMembership, Member, Group
from api.ldap import LDAPAccountManager
from ldap import LDAPError
from api.bill import BILLAccountManager, BILLException

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
    # Create LDAP and BILL accounts for given user
    member_id = request.data.get('member_id')
    member = get_object_or_404(Member, id=member_id)
    username = request.data.get('username')
    password = request.data.get('password')
    error = None
    with LDAPAccountManager() as lm:
        try:
            lm.add_account(member, username, password)

        except LDAPError as e:
            # TODO: if LDAP account already exists, try to create BILL acc?
            return Response({"LDAP": str(e)}, status=400)

    with BILLAccountManager() as bm:
        try:
            bill_code = bm.create_bill_account(username)
        except BILLException as e:
            return Response({"BILL": str(e)}, status=400)

    # Store account details
    member.username = username
    member.bill_code = bill_code
    member.save()

    # TODO: Send mail to user to notify about new accounts?

    return Response(status=200)


@api_view(['POST'])
def delete_accounts(request):
    # Delete BILL and LDAP accounts for a given user
    member_id = request.data.get('member_id')
    member = get_object_or_404(Member, id=member_id)

    with LDAPAccountManager() as lm:
        try:
            lm.delete_account(member.username)
        except LDAPError as e:
            return Response(str(e), status=400)

    bm = BILLAccountManager()
    try:
        bm.delete_bill_account(member.bill_code)
    except BILLException as e:
        return Response({"BILL": str(e)}, status=400)

    # Delete account information from user in db
    member.username = None
    member.bill_code = None
    member.save()

    return Response(status=200)


@api_view(['POST'])
def change_password(request):
    member_id = request.data.get('member_id')
    member = get_object_or_404(Member, id=member_id)
    password = request.data.get('password')

    with LDAPAccountManager() as lm:
        try:
            lm.change_password(member.username, password)
        except LDAPError as e:
            return Response(str(e), status=400)

    return Response(status=200)


@api_view(['GET'])
def get_account_info(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    result = {}
    with LDAPAccountManager() as lm:
        try:
            result['LDAP'] = {'username': member.username, 'groups': lm.get_ldap_groups(member.username)}
        except LDAPError as e:
            return Response(str(e), status=400)
    bm = BILLAccountManager()
    try:
        result['BILL'] = bm.get_bill_info(member.bill_code)
    except BILLException as e:
        return Response(str(e), status=400)

    return Response(result, status=200)
