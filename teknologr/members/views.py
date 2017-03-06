from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from members.models import *
from members.forms import *


def getCurrentYear():
    return datetime.date.today().year

def getFirstDayOfCurrentYear():
    return datetime.date(getCurrentYear(), 1, 1)

def getLastDayOfCurrentYear():
    return datetime.date(getCurrentYear(), 12, 31)

# Create your views here.s

def home_view(request):

	context = {}
	return render(request, 'base.html', context)


def set_side_context(context, category):
	side = {}
	side['active'] = category
	summary = []
	if category == 'members':
		for obj in Member.objects.all():
			summary.append({'name': obj.full_name, 'id': obj.id})
	elif category == 'groups':
		for obj in GroupType.objects.all():
			summary.append({'name': obj.name, 'id': obj.id})
	elif category == 'functionaries':
		for obj in FunctionaryType.objects.all():
			summary.append({'name': obj.name, 'id': obj.id})
	elif category == 'decorations':
		for obj in Decoration.objects.all():
			summary.append({'name': obj.name, 'id': obj.id})
	side['objects'] = summary
	context['side'] = side


def empty(request, category):
	context = {}
	set_side_context(context, category)
	return render(request, 'base.html', context)


def new_member(request):
	member = Member(given_names='Ny', surname='Medlem')
	member.save()
	return redirect('/members/{0}/'.format(member.id))


def member(request, member_id):
	context = {}

	member = get_object_or_404(Member, id=member_id)
	context['member'] = member

	if request.method == 'POST':
		form = MemberForm(request.POST, instance=member)
		if form.is_valid():
			form.save()
			context['result'] = 'success'
		else:
			context['result'] = 'failure'
	else: 
		form = MemberForm(instance=member)

	context['form'] = form
	context['full_name'] = member

	# Get functionary positions
	context['functionaries'] = Functionary.objects.filter(member__id=member_id)

	# Get groups
	context['groups'] = GroupMembership.objects.filter(member__id=member_id)

	# load side list items
	set_side_context(context, 'members')
	return render(request, 'member.html', context)


def new_group(request):
	group = GroupType()
	group.save()
	return redirect('/groups/{0}/'.format(group.id))


def group(request, grouptype_id, group_id=None):
	context = {}

	grouptype = get_object_or_404(GroupType, id=grouptype_id)
	context['grouptype'] = grouptype

	form = GroupTypeForm(instance=grouptype)

	# Get groups of group type
	context['groups'] = Group.objects.filter(grouptype__id=grouptype_id)
	context['groupTypeForm'] = form

	context['addgroupform'] = GroupForm(initial={
			"grouptype": grouptype_id,
			"begin_date": getFirstDayOfCurrentYear(),
			"end_date": getLastDayOfCurrentYear()
		})

	if group_id is not None:
		group = get_object_or_404(Group, id=group_id)
		context['group'] = group
		context['groupmembershipform'] = GroupMembershipForm(initial={"group": group_id})
		context['groupmembers'] = GroupMembership.objects.filter(group=group)

	set_side_context(context, 'groups')
	return render(request, 'group.html', context)


def new_functionarytype(request):
	functionary = FunctionaryType()
	functionary.save()
	return redirect('/functionaries/{0}/'.format(functionary.id))


def functionary(request, functionarytype_id):
	context = {}

	functionarytype = get_object_or_404(FunctionaryType, id=functionarytype_id)
	context['functionaryType'] = functionarytype
	form = FunctionaryTypeForm(instance=functionarytype)

	# Get functionaries of functionary type
	context['functionaries'] = Functionary.objects.filter(functionarytype__id=functionarytype_id)
	context['functionaryTypeForm'] = form
	context['addfunctionaryform'] = FunctionaryForm(initial={
			"functionarytype": functionarytype_id,
			"begin_date": getFirstDayOfCurrentYear(),
			"end_date": getLastDayOfCurrentYear()
		})

	set_side_context(context, 'functionaries')
	return render(request, 'functionary.html', context)


def new_decoration(request):
	decoration = Decoration()
	decoration.save()
	return redirect('/decorations/{0}/'.format(decoration.id))


def decoration(request, decoration_id):
	context = {}

	decoration = get_object_or_404(Decoration, id=decoration_id)
	context['decoration'] = decoration
	context['decorationform'] = DecorationForm(instance=decoration)

	# Get groups of group type
	context['decorations'] = DecorationOwnership.objects.filter(decoration__id=decoration_id)
	context['adddecorationform'] = DecorationOwnershipForm(initial={"decoration": decoration_id})

	set_side_context(context, 'decorations')
	return render(request, 'decoration.html', context)
