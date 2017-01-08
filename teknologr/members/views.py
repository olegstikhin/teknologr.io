from django.http import Http404
from django.shortcuts import render, get_object_or_404

from members.models import Member

# Create your views here.

def home_view(request):

	context = {}
	return render(request, 'base.html', context)

def side_members(request):
	context = {}
	members = Member.objects.all()
	summary = []
	for member in members:
		summary.append({'name': member.full_name, 'student_id': member.student_id})
	context['members'] = summary
	return render(request, 'side.html', context)

def member(request, student_id):
	context = {}
	member = get_object_or_404(Member, student_id=student_id)
	# TODO: finish this
	context['member'] = member
	return render(request, 'member.html', context)