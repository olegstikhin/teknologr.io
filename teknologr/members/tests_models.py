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
        self.assertIn("Tester", str(foobar))


class DecorationOwnerShipTest(TestCase):
    def setUp(self):
        member = Member.objects.create(given_names="Foo Bar", preferred_name="Foo", surname="Tester")
        decoration = Decoration.objects.create(name="Test Decoration")
        DecorationOwnership.objects.create(member=member, decoration=decoration, acquired=datetime.date.today())

    def test_str(self):
        dec_ownership = DecorationOwnership.objects.get(pk=1)
        self.assertIn("Test Decoration", str(dec_ownership))
        self.assertIn("Tester", str(dec_ownership))


class DecorationTest(TestCase):
    def setUp(self):
        Decoration.objects.create(name="Test Decoration")

    def test_str(self):
        decoration = Decoration.objects.get(pk=1)
        self.assertIn("Test Decoration", str(decoration))


class GroupTest(TestCase):
    def setUp(self):
        group_type = GroupType.objects.create(name="Group Type")
        Group.objects.create(grouptype=group_type,
                             begin_date=datetime.date(2016, 11, 6), end_date=datetime.date(2016, 11, 8))

    def test_str(self):
        group = Group.objects.get(pk=1)
        self.assertIn("Group Type", str(group))


class GroupTypeTest(TestCase):
    def setUp(self):
        GroupType.objects.create(name="Group Type")

    def test_str(self):
        group_type = GroupType.objects.get(name="Group Type")
        self.assertIn("Group Type", str(group_type))


class FunctionaryTest(TestCase):
    def setUp(self):
        func_type = FunctionaryType.objects.create(name="Functionary Type")
        member = Member.objects.create(given_names="Foo Bar", preferred_name="Foo", surname="Tester")
        Functionary.objects.create(functionarytype=func_type,
                                   member=member, begin_date=datetime.date(2016, 11, 4),
                                   end_date=datetime.date(2016, 11, 6))

    def test_get_str_member(self):
        func = Functionary.objects.get(pk=1)
        self.assertIn("Tester", func._get_str_member())

    def test_get_str_type(self):
        func = Functionary.objects.get(pk=1)
        self.assertIn("Functionary Type", func._get_str_type())

    def test_str(self):
        func = Functionary.objects.get(pk=1)
        self.assertIn("Tester", str(func))
        self.assertIn("Functionary Type", str(func))


class FunctionaryTypeTest(TestCase):
    def setUp(self):
        FunctionaryType.objects.create(name="Functionary Type")

    def test_str(self):
        func_type = FunctionaryType.objects.get(name="Functionary Type")
        self.assertIn("Functionary Type", str(func_type))
