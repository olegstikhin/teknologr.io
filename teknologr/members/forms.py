from members.models import *
from django.forms import ModelForm
from django.forms.widgets import CheckboxInput, DateInput

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

class GroupTypeForm(ModelForm):
    class Meta:
        model = GroupType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupTypeForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class FunctionaryTypeForm(ModelForm):
    class Meta:
        model = FunctionaryType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FunctionaryTypeForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class DecorationForm(ModelForm):
    class Meta:
        model = Decoration
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DecorationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'