from django.contrib import admin
from members.models import *

admin.site.register(Member)
admin.site.register(Group)
admin.site.register(GroupType)
admin.site.register(Functionary)
admin.site.register(FunctionaryType)
admin.site.register(GroupMembership)
admin.site.register(DecorationOwnership)