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
