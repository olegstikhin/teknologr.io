from django.db import models
from django_countries.fields import CountryField
import datetime

class SuperClass(models.Model):
    # This class is the base of everything
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class MembershipCommon(models.Model):
    # This is for all things that have a membership, for relations.

    begin_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

class Members(SuperClass):
    GENDER_CHOICES = (("MA", "Man"),("WO", "Woman"), ("UN","Unknown"))

    given_names = models.CharField(max_length=64, blank=False, null=False, default="UNKNOWN")
    preferred_name = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    surname = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    maiden_name = models.CharField(max_length=32, blank=True, null=False, default="")
    nickname = models.CharField(max_length=32, blank=True, null=False, default="")
    birth_date = models.DateField(blank=True, null=True)
    student_id = models.CharField(max_length=10, blank=True, null=False, default="")
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default="UN")
    graduated = models.BooleanField(default=False)
    graduated_year = models.IntegerField(max_length=4, blank=True, null=True)
    dead = models.BooleanField(default=False)
    mobile_phone = models.CharField(max_length=20, blank=True, null=False, default="")
    phone = models.CharField(max_length=20, blank=True, null=False, default="")
    street_address = models.CharField(max_length=64, blank=True, null=False, default="")
    postal_code = models.CharField(max_length=64, blank=True, null=False, default="")
    city = models.CharField(max_length=64, blank=True, null=False, default="")
    country = CountryField(blank_label="Välj land", blank=True, null=False, default="") # https://pypi.python.org/pypi/django-countries/1.0.1
    url = models.CharField(max_length=64, blank=True, null=False, default="")
    email = models.CharField(max_length=64, blank=True, null=False, default="")

    subscribed_to_modulen = models.BooleanField(default=False)
    allow_publish_info = models.BooleanField(default=True)

    username = models.CharField(max_length=32, blank=True, null=False, default="")
    crm_id = models.CharField(max_length=32, blank=True, null=False, default="")

    def _get_full_name(self):
        return "%s %s" % (self.given_names, self.surname)

    def _get_full_preferred_name(self):
        return "%s %s" % (self.preferred_name, self.surname)

    full_name = property(_get_full_name)
    full_preferred_name = property(_get_full_preferred_name)

    def __str__(self):
        return self.full_name


class CommitteeTypes(models.Model):
    # Committees are like groups, but they exist multiple years.
    name = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    abbrevation = models.CharField(max_length=32, blank=True, null=False, default="")
    description = models.TextField(blank=True, null=False, default="")

class Committees(SuperClass):
    name = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    abbrevation = models.CharField(max_length=32, blank=True, null=False, default="")
    begin_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    committee_type = models.ForeignKey("CommitteeTypes")
    members = models.ManyToManyField("Members", through="MembersCommitteesRelation")

class MembersCommitteesRelation(MembershipCommon):
    post_type = models.ForeignKey("PostTypes")
    member = models.ForeignKey("Members")
    committee = models.ForeignKey("Committees")


class DepartmentTypes(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    abbrevation = models.CharField(max_length=32, blank=True, null=False, default="")
    description = models.TextField(blank=True, null=False, default="")

class Departments(SuperClass):
    name = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    abbrevation = models.CharField(max_length=32, blank=True, null=False, default="")

    members = models.ManyToManyField("Members", through="MembersDepartmentsRelation")

class MembersDepartmentsRelation(MembershipCommon):
    member = models.ForeignKey("Members")
    department = models.ForeignKey("Departments")


class PostTypes(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    description = models.TextField(blank=True, null=False, default="")

class Posts(SuperClass):
    name = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    post_type = models.ForeignKey("PostTypes")
    members = models.ManyToManyField("Members", through="MembersPostsRelation")

class MembersPostsRelation(MembershipCommon):
    member = models.ForeignKey("Members")
    post = models.ForeignKey("Posts")


class Groups(SuperClass):
    # A group is a one time thing.
    name = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    year = models.IntegerField(max_length=4, blank=True, null=True)
    description = models.TextField(blank=True, null=False, default="")

    begin_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    members = models.ManyToManyField(Members, through="MembersGroupsRelation")

class MembersGroupsRelation(MembershipCommon):
    member = models.ForeignKey("Members")
    group = models.ForeignKey("Groups")
