from members.models import *
from django.forms import ModelForm
from django.forms.widgets import CheckboxInput, DateInput, HiddenInput

class BSModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BSModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if type(field.widget) is CheckboxInput:
              field.widget.attrs['class'] = 'form-check-input'
            else:
              field.widget.attrs['class'] = 'form-control'

class GroupTypeForm(BSModelForm):
    class Meta:
        model = GroupType
        fields = '__all__'

class FunctionaryTypeForm(BSModelForm):
    class Meta:
        model = FunctionaryType
        fields = '__all__'

class DecorationForm(BSModelForm):
    class Meta:
        model = Decoration
        fields = '__all__'

class GroupForm(BSModelForm):
    class Meta:
        model = Group
        fields = ['name', 'begin_date', 'end_date']

class GroupMembershipForm(BSModelForm):
    class Meta:
        model = GroupMembership
        fields = ['member']
    # TODO: some ajax search field would be necessary
