from django.db import models

# Create your models here.

class AddressInformation(models.Model):
    postal_code = models.CharField(max_length=5)
    postal_code_name_sv = models.CharField(max_length=30)
    street_name_fi = models.CharField(max_length=30)
    street_name_sv = models.CharField(max_length=30)
    municipality_name = models.CharField(max_length=20)
