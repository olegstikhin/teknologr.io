from ajax_select import register, LookupChannel
from members.models import *
from django.utils.html import escape

@register('member')
class MemberLookup(LookupChannel):

    model = Member
    
    def get_query(self, q, request):
        from django.db.models import Q

        args = []

        for word in q.split():
            args.append(Q(given_names__icontains=word) | Q(surname__icontains=word))

        if not args:
            return [] # No words in query (only spaces?)


        return Member.objects.filter(*args)

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return "%s %s" % (escape(obj.surname), escape(obj.given_names))

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "%s %s" % (escape(obj.surname), escape(obj.given_names))

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return "%s %s" % (escape(obj.surname), escape(obj.given_names))

    def check_auth(self, request):
        #TODO: Actual authentication?
        #The whole request can be denied earlier, this just limits the AJAX lookup channel? Not sure tough
        return True