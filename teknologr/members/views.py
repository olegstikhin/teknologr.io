from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from members.models import *
from members.forms import *

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
	context['member_id'] = member_id

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
	context['full_name'] = member.full_name

	# load side list items
	set_side_context(context, 'members')
	return render(request, 'member.html', context)


def delete_member(request, member_id):
	member = get_object_or_404(Member, id=member_id)
	member.delete()
	return redirect('/members/')


def new_group(request):
	group = GroupType()
	group.save()
	return redirect('/groups/{0}/'.format(group.id))


def group(request, grouptype_id, group_id=None):
	context = {}

	context['grouptype_id'] = grouptype_id
	grouptype = get_object_or_404(GroupType, id=grouptype_id)

	if request.method == 'POST':
		form = GroupTypeForm(request.POST, instance=grouptype)
		if form.is_valid():
			form.save()
			context['result'] = 'success'
		else:
			context['result'] = 'failure'
	else: 
		form = GroupTypeForm(instance=grouptype)

	# Get groups of group type
	context['groups'] = Group.objects.filter(grouptype__id=grouptype_id)
	context['form'] = form

	if group_id is not None:
		context['groupmembers'] = GroupMembership.objects.filter(group__id=group_id)

	set_side_context(context, 'groups')
	return render(request, 'group.html', context)


def delete_grouptype(request, grouptype_id):
	grouptype = get_object_or_404(GroupType, id=grouptype_id)
	# By default, django deletes all referenced foreign keys as well (on_delete=CASCADE)
	grouptype.delete()
	return redirect('/groups/')


def functionary(request, functionary_id):
	return 'TODO: implement'


def decoration(request, decoration_id):
	return 'TODO: implement'