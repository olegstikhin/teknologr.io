from django.http import Http404
from django.shortcuts import render, get_object_or_404

from members.models import Member, GroupType, FunctionaryType, Decoration
from members.forms import MemberForm

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
			summary.append({'name': obj.name, 'id': obj.name})
	elif category == 'functionaries':
		for obj in FunctionaryType.objects.all():
			summary.append({'name': obj.name, 'id': obj.name})
	elif category == 'decorations':
		for obj in Decoration.objects.all():
			summary.append({'name': obj.name, 'id': obj.name})
	side['objects'] = summary
	context['side'] = side


def empty(request, category):
	context = {}
	set_side_context(context, category)
	return render(request, 'base.html', context)


def member(request, id):
	context = {}

	if id == 'new':
		member = Member()
	else:
		member = get_object_or_404(Member, id=id)

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


def group(request, group_id):
	return 'TODO: implement'


def functionary(request, functionary_id):
	return 'TODO: implement'


def decoration(request, decoration_id):
	return 'TODO: implement'