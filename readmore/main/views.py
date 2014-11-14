from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from readmore.main.models import *
from readmore.content.views import index
from allauth.socialaccount.models import SocialAccount
from readmore.content.models import *
from django.contrib.auth.decorators import login_required
import datetime
import json

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

@login_required
def profile_self(request):
    """Return response containing the profile of the current user."""
    user = request.user
    # POSTGRESQL version
    try:
        history = ArticleHistoryItem.objects.filter(user=user)
        unique_articles = history.values('article').order_by().distinct()
        unique_articles = [art['article'] for art in unique_articles]
        history = Article.objects.filter(id__in=unique_articles)
    except Exception as e:
        print e
        history = ArticleHistoryItem.objects.filter(user=user)
    
    return render(request, 'account/profile.html', {
        "history": history
    
        })

@login_required
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

def api_get_history_totals(history, user_id=None):
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)
    if user_id is not None:
        history = history.filter(user__id=int(user_id))
    total_all = history.count()
    total_month = history.filter(date__month=date.month).count()
    total_week = history.filter(date__range=[start_week, end_week]).count()
    return HttpResponse(json.dumps({
        'week': total_week,
        'month': total_month,
        'all': total_all}), content_type='application/json')

@login_required
def api_get_total_views(request):
    user_id = request.GET.get('user', None)
    return api_get_history_totals(ArticleHistoryItem.objects, user_id)

@login_required
def api_get_total_covers(request):
    user_id = request.GET.get('user', None)
    return api_get_history_totals(WordHistoryItem.objects, user_id)

@login_required
def api_get_total_difficulty_ratings(request):
    user_id = request.GET.get('user', None)
    return api_get_history_totals(ArticleDifficultyItem.objects, user_id)

@login_required
def api_get_total_like_ratings(request):
    user_id = request.GET.get('user', None)
    return api_get_history_totals(ArticleRatingItem.objects, user_id)

@login_required
def api_get_last_events(request):
    user_id = request.GET.get('user', None)
    num = int(request.GET.get('num', 10))
    events = Event.objects
    if user_id is not None:
        events = events.filter(user__id=int(user_id))
    last_events = []
    for event in events.all()[:num]:
        last_events.append(event.describe());
    return HttpResponse(json.dumps(last_events),
            content_type='application/json')

@login_required
def api_get_most_active_users(request):
    num = int(request.GET.get('num', 10))
    users = ArticleHistoryItem.objects.values('user')
    users = users.annotate(views=Count('article')).order_by('views')
    active_users = []
    for user in users.all()[:num]:
        active_users.append({
            'user': str(User.objects.get(pk=int(user['user']))),
            'views': user['views']})
    return HttpResponse(json.dumps(active_users),
            content_type='application/json')

@login_required
def api_get_hardest_articles(request):
    user_id = request.GET.get('user', None)
    num = int(request.GET.get('num', 10))
    articles = ArticleDifficultyItem.objects.values('article', 'article__title')
    if user_id is not None:
        articles.filter(user__id=int(user_id))
    articles = articles.annotate(score=Avg('rating')).order_by('score')
    hardest_articles = []
    for article in articles.all()[:num]:
        hardest_articles.append({
            'article': {
                'url': reverse('article', args=(article['article'],)),
                'title': unicode(article['article__title']).encode(
                    'ascii', 'xmlcharrefreplace')
            },
            'rating': article['score']})
    return HttpResponse(json.dumps(hardest_articles),
            content_type='application/json')

@login_required
def api_get_favorite_articles(request):
    user_id = request.GET.get('user', None)
    num = int(request.GET.get('num', 10))
    articles = ArticleRatingItem.objects.values('article', 'article__title')
    if user_id is not None:
        articles.filter(user__id=int(user_id))
    articles = articles.annotate(score=Avg('rating')).order_by('-score')
    hardest_articles = []
    for article in articles.all()[:num]:
        hardest_articles.append({
            'article': {
                'url': reverse('article', args=(article['article'],)),
                'title': unicode(article['article__title']).encode(
                    'ascii', 'xmlcharrefreplace')
            },
            'rating': article['score']})
    return HttpResponse(json.dumps(hardest_articles),
            content_type='application/json')
