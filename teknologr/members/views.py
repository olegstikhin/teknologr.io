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

	# Get functionary positions
	context['functionaries'] = Functionary.objects.filter(member__id=member_id)

	# Get groups
	context['groups'] = GroupMembership.objects.filter(member__id=member_id)

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

	grouptype = get_object_or_404(GroupType, id=grouptype_id)
	context['grouptype'] = grouptype

	form = GroupTypeForm(instance=grouptype)

	# Get groups of group type
	context['groups'] = Group.objects.filter(grouptype__id=grouptype_id)
	context['groupTypeForm'] = form

	context['addgroupform'] = GroupForm(initial={"grouptype": grouptype_id})

	if group_id is not None:
		group = get_object_or_404(Group, id=group_id)
		context['group'] = group
		context['groupmembershipform'] = GroupMembershipForm(initial={"group": group_id})
		context['groupmembers'] = GroupMembership.objects.filter(group=group)

	set_side_context(context, 'groups')
	return render(request, 'group.html', context)


def delete_grouptype(request, grouptype_id):
	grouptype = get_object_or_404(GroupType, id=grouptype_id)
	# By default, django deletes all objects with foreign keys to this object as well (on_delete=CASCADE)
	grouptype.delete()
	return redirect('/groups/')


def add_group(request, grouptype_id):
	grouptype = get_object_or_404(GroupType, id=grouptype_id)
	group = Group(grouptype=grouptype)
	if request.method == 'POST':
		form = GroupForm(request.POST, instance=group)
		if form.is_valid():
			form.save()

	return redirect('/groups/{0}/'.format(grouptype_id))


def delete_group(request, grouptype_id, group_id):
	group = get_object_or_404(Group, id=group_id)
	group.delete()
	return redirect('/groups/{0}/'.format(grouptype_id))


def add_group_membership(request, grouptype_id, group_id):
	group = get_object_or_404(Group, id=group_id)
	membership = GroupMembership(group=group)
	if request.method == 'POST':
		form = GroupMembershipForm(request.POST, instance=membership)
		if form.is_valid():
			form.save()

	return redirect('/groups/{0}/{1}/'.format(grouptype_id, group_id))


def delete_group_membership(request, grouptype_id, group_id, membership_id):
	membership = get_object_or_404(GroupMembership, id=membership_id)
	membership.delete()
	return redirect('/groups/{0}/{1}'.format(grouptype_id, group_id))


def new_functionarytype(request):
	functionary = FunctionaryType()
	functionary.save()
	return redirect('/functionaries/{0}/'.format(functionary.id))


def delete_functionarytype(request, functionarytype_id):
	functionarytype = get_object_or_404(FunctionaryType, id=functionarytype_id)
	# By default, django deletes all objects with foreign keys to this object as well (on_delete=CASCADE)
	functionarytype.delete()
	return redirect('/functionaries/')


def functionary(request, functionarytype_id):
	context = {}

	context['functionarytype_id'] = functionarytype_id
	functionarytype = get_object_or_404(FunctionaryType, id=functionarytype_id)
	if request.method == 'POST':
		form = FunctionaryTypeForm(request.POST, instance=functionarytype)
		if form.is_valid():
			form.save()
			context['result'] = 'success'
		else:
			context['result'] = 'failure'
	else: 
		form = FunctionaryTypeForm(instance=functionarytype)

	# Get functionaries of functionary type
	context['functionaries'] = Functionary.objects.filter(functionarytype__id=functionarytype_id)
	context['form'] = form
	context['addfunctionaryform'] = FunctionaryForm()

	set_side_context(context, 'functionaries')
	return render(request, 'functionary.html', context)


def delete_decoration(request, decoration_id):
	decoration = get_object_or_404(decoration, id=decoration_id)
	# By default, django deletes all objects with foreign keys to this object as well (on_delete=CASCADE)
	decoration.delete()
	return redirect('/groups/')


def new_decoration(request):
	decoration = Decoration()
	decoration.save()
	return redirect('/decorations/{0}/'.format(decoration.id))


def decoration(request, decoration_id):
	context = {}

	context['decoration_id'] = decoration_id
	decoration = get_object_or_404(Decoration, id=decoration_id)
	if request.method == 'POST':
		form = DecorationForm(request.POST, instance=decoration)
		if form.is_valid():
			form.save()
			context['result'] = 'success'
		else:
			context['result'] = 'failure'
	else: 
		form = DecorationForm(instance=decoration)

	# Get groups of group type
	context['decorations'] = DecorationOwnership.objects.filter(decoration__id=decoration_id)
	context['form'] = form
	context['adddecorationform'] = DecorationOwnershipForm()

	set_side_context(context, 'decorations')
	return render(request, 'decoration.html', context)


def delete_decoration(request, decoration_id):
	decoration = get_object_or_404(Decoration, id=decoration_id)
	# By default, django deletes all referenced foreign keys as well (on_delete=CASCADE)
	decoration.delete()
	return redirect('/decorations/')