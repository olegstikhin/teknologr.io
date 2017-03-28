from django.test import TestCase
from members.models import Member

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
