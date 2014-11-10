from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from readmore.main.models import *
from readmore.content.views import index
from allauth.socialaccount.models import SocialAccount
from readmore.content.models import *
from django.contrib.auth.decorators import login_required


# New pages
@login_required
def history(request):
    if request.method == 'POST':
        article_id = int(request.POST.get('article', None))
        value = request.POST.get('value', None)
        history_type = request.POST.get('type', None)
        if article_id is not None and value is not None and history_type is not None:
            try:
                # Handle ratings here
                crt_article = Article.objects.get(id=article_id)
                if history_type == 'content':
                    ArticleHistoryItem.objects.create(article = crt_article, user = request.user)
                elif history_type == 'word':
                    WordHistoryItem.objects.create(article = crt_article, user = request.user, word=value)
                elif history_type == 'articlerating':
                    ArticleRatingItem.objects.create(article = crt_article, user = request.user, rating=value)
                elif history_type == 'articledifficulty':
                    ArticleDifficultyItem.objects.create(article = crt_article, user = request.user, rating=value)
                else:
                    return HttpResponse(status=400)
                
                # Ratings worked
                return HttpResponse(status=204)
            except Exception as e:
                # Bad request         
                return HttpResponse(status=400)
    # Not a post request
    return HttpResponseRedirect("/")

@login_required
def article_overview(request):
    """Return response containing overview of categories and articles."""
    # Only show top categories on the index page
    categories = Category.objects.filter(parent=None)
    articles = []
    for category in categories:
        articles += category.get_articles()
    return render(request, 'articleOverview.html', {
        "articles": articles,
        "categories": categories
    })


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
    return render(request, 'account/profile.html', {
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
