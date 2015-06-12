from django import forms
from allauth.utils import set_form_field_order
from allauth.account.forms import SignupForm
from django.utils.translation import ugettext_lazy as _

class ReadMoreSignupForm(SignupForm):
   first_name = forms.CharField(max_length=30, label= _('first name'))
   last_name = forms.CharField(max_length=30, label=_('last name'))
   code = forms.CharField(max_length=255, required=False,
           label=_('Code'))

   def __init__(self, *args, **kwargs):
       kwargs['username_required'] = False
       super(ReadMoreSignupForm, self).__init__(*args, **kwargs)
       order = self.fields.keys()
       order.remove('first_name')
       order.remove('last_name')
       set_form_field_order(self, ['first_name', 'last_name']+order)
