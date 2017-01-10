from django.http import Http404
from django.shortcuts import render, get_object_or_404

from members.models import Member, GroupType, FunctionaryType, Decoration
from members.forms import MemberForm

# Create your views here.

def home_view(request):

	context = {}
	return render(request, 'base.html', context)

def side(request, category):
	context = {'category': category}
	summary = []
	if category == 'members':
		for obj in Member.objects.all():
			summary.append({'name': obj.full_name, 'id': obj.student_id})
	elif category == 'groups':
		for obj in GroupType.objects.all():
			summary.append({'name': obj.name, 'id': obj.name})
	elif category == 'functionaries':
		for obj in FunctionaryType.objects.all():
			summary.append({'name': obj.name, 'id': obj.name})
	elif category == 'decorations':
		for obj in Decoration.objects.all():
			summary.append({'name': obj.name, 'id': obj.name})
	else:
		raise Http404

	context['objects'] = summary
	return render(request, 'side.html', context)

def member(request, student_id):
	context = {}
	member = get_object_or_404(Member, student_id=student_id)
	context['full_name'] = member.full_name
	context['form'] = MemberForm(instance=member)
	return render(request, 'member.html', context)

def group(request, group_id):
	return 'TODO: implement'

def functionary(request, functionary_id):
	return 'TODO: implement'

def decoration(request, decoration_id):
	return 'TODO: implement'