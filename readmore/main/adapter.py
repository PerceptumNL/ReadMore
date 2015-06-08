from django.conf import settings
from readmore.main.models import Group
from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponse, HttpResponseNotFound, \
        HttpResponseServerError, HttpResponseRedirect
from allauth.exceptions import ImmediateHttpResponse

class ReadMoreAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if (not settings.SIGNUP_ENABLED ):
            raise ImmediateHttpResponse(HttpResponseRedirect('/'))
        return True

    def save_user(self, request, user, form, commit=True):
        user = super(ReadMoreAccountAdapter, self).save_user(
                request, user, form, commit)
        group_code = form.cleaned_data
        if group_code:
            try:
                group = Group.objects.get(code=group_code)
            except Group.DoesNotExist:
                pass
            else:
                user.profile.groups.add(group)
                user.profile.save()
        return user
