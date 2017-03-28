import datetime

from django.test import TestCase
from members.models import *

class MemberTest(TestCase):
    def setUp(self):
        Member.objects.create(given_names="Foo Bar", preferred_name="Foo", surname="Tester")

    def test_get_full_name(self):
        foobar = Member.objects.get(given_names="Foo Bar", surname="Tester")
        self.assertEqual(foobar._get_full_name(), "Foo Bar Tester")

    def test_get_full_preferred_name(self):
        foobar = Member.objects.get(given_names="Foo Bar", surname="Tester")
        self.assertEqual(foobar._get_full_preferred_name(), "Foo Tester")

    def test_str(self):
        foobar = Member.objects.get(given_names="Foo Bar", surname="Tester")
        self.assertEqual(str(foobar), "Foo Bar Tester")

class DecorationOwnerShipTest(TestCase):
    def setUp(self):
        member = Member.objects.create(given_names="Foo Bar", preferred_name="Foo", surname="Tester")
        decoration = Decoration.objects.create(name="Test Decoration")
        DecorationOwnership.objects.create(member=member, decoration=decoration, acquired=datetime.date.today())

    def test_str(self):
        dec_ownership = DecorationOwnership.objects.get(pk=1)
        self.assertEqual(str(dec_ownership), "Test Decoration - Foo Bar Tester")

class DecorationTest(TestCase):
    def setUp(self):
        Decoration.objects.create(name="Test Decoration")

    def test_str(self):
        decoration = Decoration.objects.get(pk=1)
        self.assertEqual(str(decoration), "Test Decoration")

class GroupTest(TestCase):
    def setUp(self):
        group_type = GroupType.objects.create(name="Group Type")
        Group.objects.create(grouptype=group_type, begin_date=datetime.date(2016, 11, 6), end_date=datetime.date(2016, 11, 8))

    def test_str(self):
        group = Group.objects.get(pk=1)
        self.assertEqual(str(group), "Group Type: 2016-11-06 - 2016-11-08")
