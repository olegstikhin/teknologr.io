from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from members.models import *
from members.forms import *
from members.programmes import DEGREE_PROGRAMME_CHOICES
import datetime


def getCurrentYear():
    return datetime.date.today().year


def getFirstDayOfCurrentYear():
    return datetime.date(getCurrentYear(), 1, 1)


def getLastDayOfCurrentYear():
    return datetime.date(getCurrentYear(), 12, 31)


def getCurrentDate():
    return datetime.datetime.now()

# Create your views here

def set_side_context(context, category, active_obj=None):
    side = {}
    side['active'] = category
    side['active_obj'] = active_obj
    if category == 'members':
        side['sname'] = 'medlem'
        side['newForm'] = MemberForm(initial={'given_names': '', 'surname': ''})
        side['objects'] = [Member.objects.get(pk=active_obj)] if active_obj else []
    elif category == 'groups':
        side['sname'] = 'grupp'
        side['newForm'] = GroupTypeForm()
        side['objects'] = GroupType.objects.all()
        # summary.append({'name': obj.name, 'id': obj.id})
    elif category == 'functionaries':
        side['sname'] = 'post'
        side['newForm'] = FunctionaryTypeForm()
        side['objects'] = FunctionaryType.objects.all()
    elif category == 'decorations':
        side['sname'] = 'betygelse'
        side['newForm'] = DecorationForm()
        side['objects'] = Decoration.objects.all()
    context['side'] = side


@login_required
def empty(request, category):
    context = {}
    set_side_context(context, category)
    return render(request, 'base.html', context)

@login_required
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

    context['programmes'] = DEGREE_PROGRAMME_CHOICES
    context['form'] = form
    context['full_name'] = member

    # Get functionary positions
    context['functionaries'] = Functionary.objects.filter(member__id=member_id)
    context['addfunctionaryform'] = FunctionaryForm(initial={'member': member_id})

    # Get groups
    context['groups'] = GroupMembership.objects.filter(member__id=member_id)
    context['addgroupform'] = GroupMembershipForm(initial={'member': member_id})

    # Get membertypes
    context['membertypes'] = MemberType.objects.filter(member__id=member_id)
    context['addmembertypeform'] = MemberTypeForm(initial={'member': member_id})

    # load side list items
    set_side_context(context, 'members', member.id)
    return render(request, 'member.html', context)


@login_required
def membertype_form(request, membertype_id):
    membertype = get_object_or_404(MemberType, id=membertype_id)
    form = MemberTypeForm(instance=membertype)
    context = {'form': form, 'formid': 'editmembertypeform'}
    return render(request, 'membertypeform.html', context)


@login_required
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
        context['groupform'] = GroupForm(instance=group)
        context['groupmembershipform'] = GroupMembershipForm(initial={"group": group_id})
        context['groupmembers'] = GroupMembership.objects.filter(group=group)

    set_side_context(context, 'groups', grouptype.id)
    return render(request, 'group.html', context)


@login_required
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

    set_side_context(context, 'functionaries', functionarytype.id)
    return render(request, 'functionary.html', context)


@login_required
def decoration(request, decoration_id):
    context = {}

    decoration = get_object_or_404(Decoration, id=decoration_id)
    context['decoration'] = decoration
    context['decorationform'] = DecorationForm(instance=decoration)

    # Get groups of group type
    context['decorations'] = DecorationOwnership.objects.filter(decoration__id=decoration_id)
    context['adddecorationform'] = DecorationOwnershipForm(
        initial={"decoration": decoration_id, 'acquired': getCurrentDate()})

    set_side_context(context, 'decorations', decoration.id)
    return render(request, 'decoration.html', context)
