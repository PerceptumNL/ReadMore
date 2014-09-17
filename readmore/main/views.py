from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from readmore.main.models import *        
from allauth.socialaccount.models import SocialAccount
from readmore.content.models import *

def login(request):
    # If user already logged in, go to main site
    if request.user.is_authenticated():
        return navigation(request)
        
    # Else go to login page
    else:
        return render(request, 'login.html', 
                {
                
                }
            )

def navigation(request):
    
    allArticles = Article.objects.all()
    allCategories = Category.objects.all()
    
    
    return render(request, 'overview.html',
        {
            "articles": allArticles,
            "categories": allCategories,
        }
    )    
    
def articleNew(request):


    return render(request, 'articleView.html',
        {
        
        }
    )
    
def profileSelf(request):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return HttpResponseRedirect("/")
        
    socialaccount = SocialAccount.objects.filter(user_id=request.user.id)
    if( len(socialaccount)>0 ):
        socialaccount = socialaccount[0].extra_data
    else:
        socialaccount = {}
        
    return render(request, 'account/profileSelf.html', 
        { 
            "first_name": socialaccount.get('first_name', ''),
            "last_name": socialaccount.get('last_name', user.username),
            "age": socialaccount.get('age', '?'),
        }
    )



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
