from django.conf import settings
from readmore.main.models import Group, TeacherCode, UserProfile
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
        # Generate a UserProfile for the new user
        profile = UserProfile.objects.create(user=user)
        group_code = form.cleaned_data['group_code']
        if group_code:
            # Check if the code is a teacher code
            if TeacherCode.objects.filter(code=group_code).exists():
                group = Group.objects.create(title="Group of %s" % (user,),
                        leader=user)
            else:
                try:
                    group = Group.objects.get(code=group_code)
                except Group.DoesNotExist:
                    pass
                else:
                    profile.groups.add(group)
                    profile.save()
        return user
