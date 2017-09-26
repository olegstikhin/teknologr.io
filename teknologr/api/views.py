from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from api.serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from members.models import GroupMembership, Member, Group
from api.ldap import LDAPAccountManager
from ldap import LDAPError
from api.bill import BILLAccountManager, BILLException
from rest_framework_csv import renderers as csv_renderer

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

class LDAPAccountView(APIView):
    def get(self, request, member_id):
        member = get_object_or_404(Member, id=member_id)
        result = {}
        with LDAPAccountManager() as lm:
            try:
                result = {'username': member.username, 'groups': lm.get_ldap_groups(member.username)}
            except LDAPError as e:
                return Response(str(e), status=400)

        return Response(result, status=200)

    def post(self, request, member_id):
        # Create LDAP and BILL accounts for given user
        member = get_object_or_404(Member, id=member_id)
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response("username or password field missing", status=400)

        if member.username:
            return Response("Member already has LDAP account", status=400)

        with LDAPAccountManager() as lm:
            try:
                lm.add_account(member, username, password)
            except LDAPError as e:
                return Response(str(e), status=400)

        # Store account details
        member.username = username
        member.save()

        # TODO: Send mail to user to notify about new account?

        return Response(status=200)

    def delete(self, request, member_id):
        # Delete LDAP account for a given user
        member = get_object_or_404(Member, id=member_id)

        if not member.username:
            return Response("Member has no LDAP account", status=400)
        if member.bill_code:
            return Response("BILL account must be deleted first", status=400)

        with LDAPAccountManager() as lm:
            try:
                lm.delete_account(member.username)
            except LDAPError as e:
                return Response(str(e), status=400)

        # Delete account information from user in db
        member.username = None
        member.save()

        return Response(status=200)


@api_view(['POST'])
def change_ldap_password(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    password = request.data.get('password')
    if not password:
        return Response("password field missing", status=400)

    with LDAPAccountManager() as lm:
        try:
            lm.change_password(member.username, password)
        except LDAPError as e:
            return Response(str(e), status=400)

    return Response(status=200)


class BILLAccountView(APIView):
    def get(self, request, member_id):
        member = get_object_or_404(Member, id=member_id)

        if not member.bill_code:
            return Response("Member has no BILL account", status=400)

        bm = BILLAccountManager()
        try:
            result = bm.get_bill_info(member.bill_code)
        except BILLException as e:
            return Response(str(e), status=400)

        return Response(result, status=200)

    def post(self, request, member_id):
        member = get_object_or_404(Member, id=member_id)

        if member.bill_code:
            return Response("BILL account already exists", status=400)
        if not member.username:
            return Response("LDAP account missing", status=400)

        bm = BILLAccountManager()
        try:
            bill_code = bm.create_bill_account(member.username)
        except BILLException as e:
            return Response(str(e), status=400)

        member.bill_code = bill_code
        member.save()

        return Response(status=200)

    def delete(self, request, member_id):
        member = get_object_or_404(Member, id=member_id)

        if not member.bill_code:
            return Response("Member has no BILL account", status=400)

        bm = BILLAccountManager()
        try:
            bm.delete_bill_account(member.bill_code)
        except BILLException as e:
            return Response(str(e), status=400)

        member.bill_code = None
        member.save()

        return Response(status=200)


# JSON API:s

# Used by BILL
@api_view(['GET'])
def memberTypesForMember(request, mode, query):

    try:
        if mode == 'username':
            member = Member.objects.get(username=query)
        elif mode == 'studynumber':
            member = Member.objects.get(student_id=query)
        else:
            return Response(status=400)
    except Member.DoesNotExist as e:
        return Response(status=200)

    membertypes = {}

    for e in MemberType.objects.filter(member=member):
        membertypes[e.type] = (str(e.begin_date), str(e.end_date))

    data = {
        "given_names": member.given_names.split(),
        "surname": member.surname,
        "nickname": member.nickname,
        "preferred_name": member.preferred_name,
        "membertypes": membertypes
    }

    return Response(data, status=200)


# Used by GeneriKey
@api_view(['GET'])
def membersByMemberType(request, membertype, field=None):
    member_pks = MemberType.objects.filter(type=membertype, end_date=None).values_list("member", flat=True)
    fld = "username" if field == "usernames" else "student_id"
    members = Member.objects.filter(pk__in=member_pks).values_list(fld, flat=True)
    return Response(members, status=200)


# Data for HTK
@api_view(['GET'])
def htkDump(request, member=None):
    def dumpMember(member):
        funcs = Functionary.objects.filter(member=member)
        flist = []
        for f in funcs:
            flist.append(",".join([f.functionarytype.name, str(f.begin_date), str(f.end_date)]))

        groups = GroupMembership.objects.filter(member=member)
        glist = []
        for g in groups:
            glist.append(",".join([g.group.grouptype.name, str(g.group.begin_date), str(g.group.end_date)]))
        
        types = MemberType.objects.filter(member=member)
        tlist = []
        for t in types:
            tlist.append(",".join([t.get_type_display(), str(t.begin_date), str(t.end_date)]))

        return {
            "name": member.full_name,
            "functionaries": flist,
            "groups": glist,
            "membertypes": tlist
        }

    if member:
        m = get_object_or_404(Member, id=member)
        data = dumpMember(m)
    else:
        data = [dumpMember(m) for m in Member.objects.all()]

    return Response(data, status=200)

#CSV-render class
class ModulenRenderer(csv_renderer.CSVRenderer):
    header = ['name', 'address']

# List of addresses whom to post modulen to
@api_view(['GET'])
@renderer_classes((ModulenRenderer,))
def modulenDump(request):

    recipients = Member.objects.exclude(
            postal_code='02150'
        ).exclude(
            dead=True
        ).filter(
            subscribed_to_modulen=True
        )

    content = [{
        'name': recipient._get_full_name(),
        'address': recipient._get_full_address()}
        for recipient in recipients]


    return Response(content, status=200)