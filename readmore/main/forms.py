from django import forms
from allauth.account.forms import SignupForm
from django.utils.translation import ugettext_lazy as _

class ReadMoreSignupForm(SignupForm):
   group_code = forms.CharField(max_length=255, required=False,
           label=_('Group code'))
