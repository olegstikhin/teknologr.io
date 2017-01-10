from members.models import Member
from django.forms import ModelForm
from django.forms.widgets import CheckboxInput

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