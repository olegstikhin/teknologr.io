# -*- coding: utf-8 -*-

from django.db.models import Q
from members.models import Member, MemberType
from datetime import date


def findMembers(query, count=50):

    args = []

    for word in query.split():
        args.append(Q(given_names__icontains=word) | Q(surname__icontains=word))

    if not args:
        return []  # No words in query (only spaces?)

    return Member.objects.filter(*args).order_by('surname', 'given_names')[:count]

def findMostRecentMemberTypeAndYear(member):

	types = MemberType.objects.filter(member=member).order_by()

	if (len(types)) == 0:
		return 'No types'

	ordinarie = next((x for x in types if x.type == "OM"), None)
	if ordinarie and not ordinarie.end_date:
		return str(ordinarie)

	stalm = next((x for x in types if x.type == "ST"), None)
	if stalm and not stalm.end_date:
		return str(stalm)

	return 'Varken stälm eller ordinarie'
