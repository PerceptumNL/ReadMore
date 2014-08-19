from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from readmore.main.models import *        
        
def profile(request, user_id):
    try:
        user = User.objects.get(username=user_id)
    except User.DoesNotExist:
        return HttpResponseRedirect("/")
        
    badges = Badge.objects.filter(userprofile=user)
    if not badges:
        badges = []
        
    try:
        statistics = Statistics.objects.get(user=user)
    except Statistics.DoesNotExist:
        statistics = Statistics.objects.create(user=user)
    
   
    return render(request, 'account/profile.html', 
        { 
            "user_details": user,
            "badges": badges,
            "statistics": statistics,
            
        }
    )
