from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from readmore.main.models import *
from readmore.content.views import index
from allauth.socialaccount.models import SocialAccount
from readmore.content.models import *

def error(request):
    """Raise an exception."""
    from django.core.mail import send_mail
    send_mail('Test subject', 'An error is on its way.',
            'readmore-platform-manual@perceptum.nl',
            ['sanderlatour@gmail.com'], fail_silently=False)
    raise Exception('Some error occured.')

def login(request):
    # If user already logged in, go to main site
    if request.user.is_authenticated():
        return index(request)
    # Else go to login page
    else:
        return render(request, 'login.html',{})

def profile_self(request):
    """Return response containing the profile of the current user."""
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect("/")
    socialaccount = SocialAccount.objects.filter(user_id=request.user.id)
    if( len(socialaccount)>0 ):
        socialaccount = socialaccount[0].extra_data
    else:
        socialaccount = {}
    return render(request, 'account/profileSelf.html', {
            "first_name": socialaccount.get('first_name', ''),
            "last_name": socialaccount.get('last_name', user.username),
            "age": socialaccount.get('age', '?')})

def profile(request, user_id):
    """Return response containing the profile of the given user."""
    try:
        user = User.objects.get(username=user_id)
    except User.DoesNotExist:
        return HttpResponseRedirect("/")
    # Retrieve badges
    badges = Badge.objects.filter(userprofile=user)
    if not badges:
        badges = []
    badges = [badge.current_image(user) for badge in badges]
    # Retrieve google image, if any
    google_uid = SocialAccount.objects.filter(
            user_id=user.id, provider='google')
    if google_uid:
        google_image = google_uid[0].extra_data['picture']
    else:
        google_image = ""
    # Retrieve statistics
    try:
        statistics = Statistics.objects.get(user=user)
    except Statistics.DoesNotExist:
        statistics = Statistics.objects.create(user=user)
    # Retrieve article history
    article_history = History.objects.filter(user=user)
    # Render response
    return render(request, 'account/profile.html',{
            "user_details": user,
            "badges": badges,
            "statistics": statistics,
            "profileImage": google_image,
            "articleHistory": article_history})

def about(request):
    return render(request, 'about.html')
