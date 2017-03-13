from ajax_select import register, LookupChannel
from members.models import *
from django.utils.html import escape

@register('member')
class MemberLookup(LookupChannel):

    model = Member
    
    def get_query(self, q, request):
        from django.db.models import Q
        '''Search queries are expected to be of type:
        Surname 1st 2nd ...
        where 1st,2nd are firstnames (need not be in that specific order)
        '''
        
        split = q.split()

        if not split:
            #"Empty" search query (might have been only spaces)
            return []

        surname = split[0]
        firstnames = split[1:]

        surnames = Member.objects.filter(surname__icontains=surname)

        if not firstnames:
            return surnames

        res = []

        for name in firstnames:#Somehow fix this
            res += surnames.filter(given_names__icontains=name).exclude(id__in=[x.id for x in res])

        return res

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