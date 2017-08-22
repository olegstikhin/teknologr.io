# -*- coding: utf-8 -*-

import csv
from django.core.management.base import NoArgsCommand
from members.models import *
from datetime import date
from django.db import IntegrityError


def get_date(datestr):
    return datestr.split()[0] if datestr else None


def get_gender(gender):
    if gender is "1":
        return "M"
    elif gender is "2":
        return "F"
    else:
        return "UN"


def get_country(country):
    if not country:
        return ""
    country = country.lower()
    if country in ['fi', 'fin']:
        return "FI"
    if country in ['bz']:
        return "BR"
    if country in ['da']:
        return "DK"
    if country in ['es']:
        return "ES"
    if country in ['fr']:
        return "FR"
    if country in ['no']:
        return "NO"
    if country in ['ru']:
        return "RU"
    if country in ['po']:
        return "PU"
    if country in ['se', 'sv']:
        return "SE"
    if country in ['ty']:
        return "DE"
    return ""


def get_address_country(country):
    countries = {
        "Belgium": "BE",
        "Chile": "CL",
        "Colombia": "CO",
        "Costa Rica": "CR",
        "Croatia": "HR",
        "Danmark": "DK",
        "Deutschland": "DE",
        "England": "GB",
        "Estland": "EE",
        "FIN": "FI",
        "Finland": "FI",
        "France": "FR",
        "Frankrike": "FR",
        "Germany": "DE",
        "GERMANY": "DE",
        "Helsingfors": "FI",
        "Kanada": "CA",
        "Luxembourg": "LU",
        "Norge": "NO",
        "Polen": "PL",
        "Schweiz": "CH",
        "Spain": "ES",
        "Sverige": "SE",
        "Switzerland": "CH",
        "The Netherlands": "NL",
        "Tyskland": "DE",
        "United Kingdom": "GB",
        "United States": "US",
        "USA": "US",
        "Vasa": "FI"
    }
    return countries[country] if country in countries else ""


def get_enrol_year(year):
    yr = int(year.split()[0])
    return None if yr == 9999 else yr


def get_bool(val):
    return False if val is None or val is "" else bool(int(val))


class Command(NoArgsCommand):

    help = "Whatever you want to print here"

    def handle_noargs(self, **options):
        with open('alltut.csv') as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            headers = None
            for row in reader:
                if not headers:
                    headers = row
                    continue
                data = dict(zip(headers, row))
                member = Member()
                member.given_names = data["givenNames_fld"]
                member.preferred_name = data["preferredName_fld"]
                member.surname = data["surName_fld"]
                member.maiden_name = data["maidenName_fld"]
                member.nickname = data["nickName_fld"]
                member.birth_date = get_date(data["birthDate_fld"])
                member.student_id = data["studentId_fld"]
                member.gender = get_gender(data["gender_fld"])
                member.nationality = get_country(data["nationality_fld"])
                # member.enrolment_year = get_enrol_year(data["första år samt medlemskapstyp"])
                member.graduated = get_bool(data["graduated_fld"])
                # member.graduated_year = int(data[""])
                # member.degree_programme = data[""]
                member.dead = get_bool(data["dead_fld"])
                member.mobile_phone = data["cellPhone_fld"]
                member.phone = data["phone_fld"]
                member.street_address = data["streetAddress_fld"]
                member.postal_code = data["postalCode_fld"]
                member.city = data["city_fld"]
                member.country = get_address_country(data["country_fld"])
                member.url = data["url_fld"]
                member.email = data["email_fld"]
                member.subscribed_to_modulen = get_bool(data["subscribedtomodulen_fld"])
                member.allow_publish_info = not get_bool(data["noPublishContactInfo_fld"])
                member.username = data["username_fld"]
                # member.bill_code = data[""]
                # member.crm_id = data[""]
                member.comment = data["notes_fld"]
                member.save()

                # Groups
                groups = data['grupper'].split(",")
                groups.remove("")
                for group in groups:
                    name, year = group.rsplit(" ", 1)
                    year = int(year)
                    if name == "Abikommittén":
                        name = "TF Rekry"
                    elif name == "InfoK / CyberK":
                        name = "CyberK"
                    gt, vask = GroupType.objects.get_or_create(name=name)
                    begin = date(year, 1, 1)
                    end = date(year, 12, 31)
                    group_model, vask = Group.objects.get_or_create(grouptype=gt, begin_date=begin, end_date=end)
                    try:
                        GroupMembership.objects.create(member=member, group=group_model)
                    except IntegrityError as e:

                        if 'unique constraint' in e.args[0].lower():
                            continue
                        else:
                            raise e

