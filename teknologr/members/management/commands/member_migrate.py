# -*- coding: utf-8 -*-

import csv
from django.core.management.base import NoArgsCommand
from members.models import *
import datetime
from django.db import IntegrityError
import re

dateformat = "%Y-%m-%d %H:%M:%S"

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

def get_decorations(notes):
    if not notes:
        return []

    decorationnames = {
        "Förtjänsttecken": ["Förtjänsttecken", "TF:s förtjänsttecken", "Förtjänstecken", "Fortjansttecken"],
        "Hederstecken i silver": ["HTsilver", "HT silver", "HT Silver", "Hederstecken i silver", "Hedersmärke i silver", "TFs hedersmärke i silver", "hederstecken i silver"],
        "Hederstecken i guld": ["HTguld", "HT guld", "Hedersmärke i guld", "Hedersmärke i Guld"],
        "Hedersmedlem": ["Hedersmedlem"],
        "Stavans kamratskapsmärke": ["Stavans kamratskapsmärke"]
    }
    regexend = r" (?:(\d{4}|\(\d{2}\)|\(\d{4}\)|\d{1,2}\.\d{1,2}\.\d{4}))"
    decorations = []
    for decoration, names in decorationnames.items():
        for name in names:
            if name in notes:
                try:
                    pattern = name + regexend
                    m = re.search(pattern, notes)
                    if m is not None:
                        year = m.group(1)
                    else:
                        year = "None"
                    if year[0] == '(':
                        year = year[1:-1] # Remove parentheses
                    if len(year) == 2:
                        if year[0] == '0' or year[0] == '1':
                            # We assume no two digit year entries from 1900s or 1910s
                            year = "20" + year
                        else:
                            year = "19" + year
                    decorations.append((decoration, year))
                except Exception as e:
                    print(m)
                    print(pattern)
                    print(notes)
                    raise e

    return decorations


def get_enrol_year(year):
    yr = int(year.split()[0])
    return None if yr == 9999 else yr


def get_bool(val):
    return False if val is None or val is "" else bool(int(val))

def get_mandates(begin, end):
    # NOTE: need to pip install python-dateutil
    # Did not want to include this in requirements.txt as this is a run-once migration script.
    from dateutil.relativedelta import relativedelta
    # TODO: vissa mandattider som går över årsskfitet ska splittas, andra int? (t.ex. arbetsgrupper)
    length = relativedelta(end, begin)
    mandates = []
    while length.years > 1 or (length.years == 1 and (length.months > 0 or length.days > 0)):
        mandates.append((begin, datetime.date(begin.year, 12, 31)))
        begin = datetime.date(begin.year + 1, 1, 1)
        length = relativedelta(end, begin)
    mandates.append((begin, end))
    return mandates



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

                # Member
                member = Member()
                names = data["givenNames_fld"]
                prefname = data["preferredName_fld"]
                member.given_names = names if names != "" else prefname
                member.preferred_name = prefname
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
                for group in groups:
                    if not group:
                        continue
                    name, startt, endt = group.split(";")
                    if name == "Abikommittén":
                        name = "TF Rekry"
                    elif name == "InfoK / CyberK":
                        name = "CyberK"

                    gt, vask = GroupType.objects.get_or_create(name=name)
                    startt = startt.split(".")[0] if "." in startt else startt
                    endt = endt.split(".")[0] if "." in endt else endt
                    begin = datetime.datetime.strptime(startt, dateformat).date() if startt != "None" else None
                    end = datetime.datetime.strptime(endt, dateformat).date() if endt != "None" else None
                    
                    # Split multi year mandates to single years
                    mandates = get_mandates(begin, end)

                    for m in mandates:
                        begin, end = m
                        # We need a single group for all overlapping membership times
                        group_models = Group.objects.filter(
                            grouptype=gt,
                            begin_date__lt=end,
                            end_date__gt=begin)

                        c = group_models.count()
                        if c == 0:
                            group_model = Group.objects.create(grouptype=gt, begin_date=begin, end_date=end)
                        elif c > 1:
                            print("mandate: {}: {} - {}".format(gt, begin, end))
                            for g in group_models:
                                print(g)
                            raise Exception()
                        else:
                            group_model = group_models[0]
                        if group_model.begin_date != begin or group_model.end_date != end:
                            if group_model.begin_date != begin:
                                group_model.begin_date = begin
                            if group_model.end_date != end:
                                group_model.end_date = end
                            group_model.save()

                        try:
                            GroupMembership.objects.create(member=member, group=group_model)
                        except IntegrityError as e:
                            if 'unique constraint' in e.args[0].lower():
                                # Duplicates? ignore.
                                continue
                            else:
                                raise e

                # Functionaries
                funcs = data['poster'].split(",")
                for func in funcs:
                    if not func:
                        continue
                    name, startt, endt = func.split(";")

                    if name == "Spexdirecteur":
                        name = "Spexdirektör"

                    ft, vask = FunctionaryType.objects.get_or_create(name=name)
                    startt = startt.split(".")[0] if "." in startt else startt
                    endt = endt.split(".")[0] if "." in endt else endt
                    begin = datetime.datetime.strptime(startt, dateformat).date() if startt != "None" else None
                    end = datetime.datetime.strptime(endt, dateformat).date() if endt != "None" else None
                    try:
                        Functionary.objects.create(member=member, functionarytype=ft, begin_date=begin, end_date=end)
                    except IntegrityError as e:
                        if 'unique constraint' in e.args[0].lower():
                            # Duplicates? ignore.
                            continue
                        else:
                            raise e

                # Decorations
                decs = get_decorations(data['notes_fld'])
                for dec in decs:
                    name, dat = dec
                    decoration, vask = Decoration.objects.get_or_create(name=name)
                    if dat == "None":
                        # TODO: what date? field is NOT NULL
                        acquired = date(1900, 1, 1)
                    elif '.' in dat:
                        day, month, year = [int(nr) for nr in dat.split('.')]
                        acquired = date(year, month, day)
                    else:
                        year = int(dat)
                        acquired = date(year, 3, 18)
                    DecorationOwnership.objects.create(member=member, decoration=decoration, acquired=acquired)

                # MemberTypes



