from django.db import models
from django_countries.fields import CountryField
import datetime

def getEpoch():
	return datetime.date(1872, 1, 1)

class SuperClass(models.Model):
    # This class is the base of everything
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Member(SuperClass):
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

class DecorationOwnership(SuperClass):
	member = models.ForeignKey("Member")
	decoration = models.ForeignKey("Decoration")
	acquired = models.DateField(default=getEpoch())

class Decoration(SuperClass):
	name = models.CharField(max_length=64, blank=False, null=False, unique=True)

class GroupMembership(SuperClass):
	member = models.ForeignKey("Member")
	group = models.ForeignKey("Group")
	begin_date = models.DateField(default=getEpoch())
	end_date = models.DateField(default=getEpoch())

class Group(SuperClass):
	name = models.CharField(max_length=64, blank=False, null=False, unique=True)
	grouptype = models.ForeignKey("GroupType")
	begin_date = models.DateField(default=getEpoch())
	end_date = models.DateField(default=getEpoch())	

class GroupType(SuperClass):
	name = models.CharField(max_length=64, blank=False, null=False, unique=True)

class Functionary(SuperClass):
	name = models.CharField(max_length=64, blank=False, null=False, unique=True)
	member = ForeignKey("Member")
	functionarytype = ForeignKey("FunctionaryType")
	begin_date = models.DateField(default=getEpoch())
	end_date = models.DateField(default=getEpoch())

class FunctionaryType(SuperClass):
	name = models.CharField(max_length=64, blank=False, null=False, unique=True)

