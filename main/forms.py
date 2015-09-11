from django import forms
from allauth.utils import set_form_field_order
from allauth.account.forms import SignupForm
from django.utils.translation import ugettext_lazy as _

from .models import TeacherCode, Group

class ReadMoreSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label= _('First Name'),
            widget=forms.TextInput(attrs={'placeholder': _('First Name')}))
    last_name = forms.CharField(max_length=30, label=_('Last Name'),
            widget=forms.TextInput(attrs={'placeholder': _('Last Name')}))
    code = forms.CharField(max_length=255, required=True, label=_('Code'),
            widget=forms.TextInput(attrs={'placeholder': _('Code')}))

    def __init__(self, *args, **kwargs):
       kwargs['username_required'] = False
       super(ReadMoreSignupForm, self).__init__(*args, **kwargs)
       order = self.fields.keys()
       order.remove('first_name')
       order.remove('last_name')
       set_form_field_order(self, ['first_name', 'last_name']+order)

    def clean(self):
        super(SignupForm, self).clean()
        code = self.cleaned_data['code']
        if not TeacherCode.objects.filter(active=True, code=code).exists() or \
                not Group.objects.filter(code=code).exists():
                    raise forms.ValidationError(_("This code is not known."))
        return self.cleaned_data
