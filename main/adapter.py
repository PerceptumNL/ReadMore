from django.conf import settings
from main.models import Group, TeacherCode, UserProfile
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
        code = form.cleaned_data['code']
        if code:
            # Check if the code is a teacher code
            try:
                code_obj = TeacherCode.objects.get(code=code)
            except TeacherCode.DoesNotExist:
                try:
                    group = Group.objects.get(code=code)
                except Group.DoesNotExist:
                    pass
                else:
                    profile.institute = group.institute
                    profile.groups.add(group)
                    profile.code = group.leader.userprofile.code
                    profile.save()
            else:
                group = Group.objects.create(title="Group of %s" % (user,),
                        leader=user, institute=code_obj.institute)
                profile.institute = code_obj.institute
                profile.code = code_obj
                profile.is_teacher = True
                profile.save()
        return user
