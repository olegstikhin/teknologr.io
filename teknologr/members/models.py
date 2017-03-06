from django.db import models
from django_countries.fields import CountryField


class SuperClass(models.Model):
    # This class is the base of everything
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Member(SuperClass):
    GENDER_CHOICES = (("UN","Okänd"), ("M", "Man"),("F", "Kvinna"))
    DEGREE_PROGRAMME_CHOICES = (
        ('UN', 'Okänd'),
        ('ARTS - Högskolan för konst, design och arkitektur', (
            ('ARK', 'Arkitektur'),
            ('BP', 'Bildkonstpedagogik'),
            ('DS', 'Design'),
            ('DK', 'Dokumentärfilm'),
            ('FM', 'Film- och tv-manuskript'),
            ('FP', 'Film- och tv-produktion'),
            ('FS', 'Film- och tv-scenografi'),
            ('FK', 'Filmklippning'),
            ('FL', 'Filmljudinspelning och -ljudplanering'),
            ('FI', 'Filmning'),
            ('FR', 'Filmregi'),
            ('GD', 'Grafisk design'),
            ('IA', 'Inredningsarkitektur'),
            ('KD', 'Kostymdesign'),
            ('LA', 'Landskapsarkitektur'),
            ('MD', 'Mode'),
            ('TS', 'Teaterscenografi'),
        )),
        ('BIZ - Handelshögskolan', (
            ('KT', 'Kauppatieteet'),
        )),
        ('CHEM - Högskolan för kemiteknik', (
            ('KB', 'Kemi-, bio- och materialteknik'),
        )),
        ('ELEC - Högskolan för elektroteknik', (
            ('AI', 'Automations- och informationsteknologi'),
            ('BI', 'Bioinformationsteknologi'),
            ('EL', 'Elektronik och elektroteknik'),
        )),
        ('ENG - Högskolan för ingenjörsvetenskaper', (
            ('BM', 'Den byggda miljön'),
            ('EM', 'Energi- och miljöteknik'),
            ('MB', 'Maskin- och byggnadsteknik'),
        )),
        ('SCI - Högskolan för teknikvetenskaper', (
            ('DT', 'Datateknik'),
            ('IN', 'Informationsnätverk'),
            ('PE', 'Produktionsekonomi'),
            ('TF', 'Teknisk fysik och matematik'),
        ))
    )

    given_names = models.CharField(max_length=64, blank=False, null=False, default="UNKNOWN")
    preferred_name = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    surname = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    maiden_name = models.CharField(max_length=32, blank=True, null=False, default="")
    nickname = models.CharField(max_length=32, blank=True, null=False, default="")
    birth_date = models.DateField(blank=True, null=True)
    student_id = models.CharField(max_length=10, blank=True, null=False, default="")
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default="UN")
    nationality = CountryField(blank_label="Välj land", blank=True, null=False, default="") # https://pypi.python.org/pypi/django-countries/1.0.1
    enrolment_year = models.IntegerField(blank=True, null=True)
    graduated = models.BooleanField(default=False)
    graduated_year = models.IntegerField(blank=True, null=True)
    degree_programme = models.CharField(max_length=256, choices=DEGREE_PROGRAMME_CHOICES, default="UN")
    stalm = models.BooleanField(default=False)
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
    comment = models.TextField(blank=True, null=True)

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
    acquired = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.decoration.name, self.member.full_name)

class Decoration(SuperClass):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

class GroupMembership(SuperClass):
    member = models.ForeignKey("Member")
    group = models.ForeignKey("Group")

class Group(SuperClass):
    grouptype = models.ForeignKey("GroupType")
    begin_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "{0} - {1}, {2}".format(self.begin_date, self.end_date, self.grouptype.name)

class GroupType(SuperClass):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

class Functionary(SuperClass):
    member = models.ForeignKey("Member")
    functionarytype = models.ForeignKey("FunctionaryType")
    begin_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
    	return "{0} - {1}, {2}".format(self.begin_date, self.end_date, self.member)

class FunctionaryType(SuperClass):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name
