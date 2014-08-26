from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from readmore.main.models import *        
from allauth.socialaccount.models import SocialAccount

def profile(request, user_id):
    try:
        user = User.objects.get(username=user_id)
    except User.DoesNotExist:
        return HttpResponseRedirect("/")
        
    badges = Badge.objects.filter(userprofile=user)
    if not badges:
        badges = []
    badges = [badge.current_image(user) for badge in badges]
        
    google_uid = SocialAccount.objects.filter(user_id=user.id, provider='google')  
    google_image = ""
    if len(google_uid):
        google_image = google_uid[0].extra_data['picture']
        
    try:
        statistics = Statistics.objects.get(user=user)
    except Statistics.DoesNotExist:
        statistics = Statistics.objects.create(user=user)
    
   
    article_history = []
    try:
        article_history = History.objects.filter(user=user)
    except:
        # No user history
        pass
   
    return render(request, 'account/profile.html', 
        { 
            "user_details": user,
            "badges": badges,
            "statistics": statistics,
            "profileImage": google_image,
            "articleHistory": article_history,
            
        }
    )
