from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from django.http import HttpResponse, HttpResponseRedirect, \
        HttpResponseBadRequest, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from main.models import *
from content.models import *
from allauth.socialaccount.models import SocialAccount
import datetime
import json
import pytz

from django.core.mail import send_mail

def show_technical_report(request):
    from django.views.debug import technical_500_response
    return technical_500_response(request)

def pilot_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        school = request.POST.get('school', "onbekend")
        function = request.POST.get('function', "onbekend")
        if email:
            try:
                pilotSignup = PilotSignup.objects.create(
                        email=email, school=school, function=function)
                pilotSignup.save()
                textbody = email + "\n" + function + " op " + school
                send_mail('Nieuwe pilot signup', textbody,
                        'no-reply@leestmeer.nl',
                        ['robrecht@leestmeer.nl', 'david@leestmeer.nl'])
                return HttpResponseRedirect('www.leestmeer.nl', status=204)
            except Exception:
                # Bad request
                return HttpResponse(status=400)

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
def dashboard_dispatch(request):
    teacher = request.GET.get('teacher', None)
    if request.user.is_superuser and teacher is not None:
        from django.contrib.auth import get_user_model
        user = get_object_or_404(get_user_model(), pk=teacher)
    else:
        user = request.user

    groups = user.teaches.count()
    if groups == 1:
        from teacher.views import dashboard_group
        return dashboard_group(request, user.teaches.get().pk)
    elif groups > 1:
        from teacher.views import dashboard_main
        return dashboard_main(request)
    else:
        return profile_self(request)

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
        history = ArticleHistoryItem.objects.filter(user=user)

    return render(request, 'account/profile.html', {
        "history": history,
        "group": request.user.userprofile.groups.first()
    })

@login_required
def profile(request, user_id):
    """Return response containing the profile of the given user."""
    try:
        user = User.objects.get(username=user_id)
    except User.DoesNotExist:
        return HttpResponseRedirect("/")
    # Retrieve badges
    badges = user.userprofile.badges.all()
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

def filter_on_period(objects, period):
    if period == 'month':
        date = datetime.datetime.now(pytz.utc)
        return objects.filter(date__month=date.month)
    elif period == 'week':
        date = datetime.datetime.now(pytz.utc)
        date -= datetime.timedelta(hours=date.hour)
        date -= datetime.timedelta(minutes=date.minute)
        date -= datetime.timedelta(seconds=date.second)
        date -= datetime.timedelta(microseconds=date.microsecond)
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        return objects.filter(date__range=[start_week, end_week])
    else:
        return objects

@login_required
def api_group(request):
    if request.method == "POST":
        if request.user.userprofile.groups.count() > 0:
            return HttpResponseForbidden()
        code = request.POST.get('code', '')
        if not code:
            return HttpResponseBadRequest()
        group = get_object_or_404(Group, code=code)
        request.user.userprofile.groups.add(group)
        request.user.userprofile.save()
        return HttpResponse()
    else:
        return HttpResponse(status=405)

@login_required
def api_get_history_totals(request, history, user_id=None):
    if user_id:
        history = history.filter(user__id=int(user_id))
    if not request.user.is_superuser:
        history = history.filter(user__userprofile__groups__leader=request.user)
    total_all = filter_on_period(history, 'all').count()
    total_month = filter_on_period(history, 'month').count()
    total_week = filter_on_period(history, 'week').count()
    return HttpResponse(json.dumps({
        'week': total_week,
        'month': total_month,
        'all': total_all}), content_type='application/json')

@login_required
def api_get_total_views(request):
    user_id = request.GET.get('user', None)
    return api_get_history_totals(request, ArticleHistoryItem.objects, user_id)

@login_required
def api_get_total_covers(request):
    user_id = request.GET.get('user', None)
    return api_get_history_totals(request, WordHistoryItem.objects, user_id)

@login_required
def api_get_total_difficulty_ratings(request):
    user_id = request.GET.get('user', None)
    return api_get_history_totals(request, ArticleDifficultyItem.objects, user_id)

@login_required
def api_get_total_like_ratings(request):
    user_id = request.GET.get('user', None)
    return api_get_history_totals(request, ArticleRatingItem.objects, user_id)

@login_required
def api_get_last_events(request):
    user_id = request.GET.get('user', None)
    num = int(request.GET.get('num', 10))
    events = Event.objects
    if user_id:
        events = events.filter(user__id=int(user_id))
    if not request.user.is_superuser:
        events = events.filter(user__userprofile__groups__leader=request.user)
    last_events = []
    for event in events.all()[:num]:
        last_events.append(event.describe());
    return HttpResponse(json.dumps(last_events),
            content_type='application/json')

@login_required
def api_get_most_active_users(request):
    num = int(request.GET.get('num', 10))
    period = request.GET.get('period', 'all')
    users = ArticleHistoryItem.objects.values('user')
    if not request.user.is_superuser:
        users = users.filter(user__userprofile__groups__leader=request.user)
    users = filter_on_period(users, period)
    users = users.annotate(views=Count('article')).order_by('views')
    active_users = []
    displayname = (lambda user: u' '.join([user.first_name, user.last_name])
            if user.first_name else user.username)
    for user in users.all()[:num]:
        active_users.append({
            'user': displayname(User.objects.get(pk=int(user['user']))),
            'views': user['views']})
    return HttpResponse(json.dumps(active_users),
            content_type='application/json')

@login_required
def api_get_hardest_articles(request):
    user_id = request.GET.get('user', None)
    num = int(request.GET.get('num', 10))
    period = request.GET.get('period', 'all')
    articles = ArticleDifficultyItem.objects.values('article', 'article__title')
    articles = filter_on_period(articles, period)
    if user_id:
        articles = articles.filter(user__id=int(user_id))
    if not request.user.is_superuser:
        articles = articles.filter(
                user__userprofile__groups__leader=request.user)
    articles = articles.annotate(score=Avg('rating')).order_by('score')
    hardest_articles = []
    for article in articles.all()[:num]:
        hardest_articles.append({
            'article': {
                'url': reverse('article', args=(article['article'],)),
                'title': unicode(article['article__title'])
            },
            'rating': article['score']})
    return HttpResponse(json.dumps(hardest_articles),
            content_type='application/json')

@login_required
def api_get_favorite_articles(request):
    user_id = request.GET.get('user', None)
    num = int(request.GET.get('num', 10))
    period = request.GET.get('period', 'all')
    articles = ArticleRatingItem.objects.values('article', 'article__title')
    articles = filter_on_period(articles, period)
    if user_id:
        articles = articles.filter(user__id=int(user_id))
    if not request.user.is_superuser:
        articles = articles.filter(
                user__userprofile__groups__leader=request.user)
    articles = articles.annotate(score=Avg('rating')).order_by('-score')
    hardest_articles = []
    for article in articles.all()[:num]:
        hardest_articles.append({
            'article': {
                'url': reverse('article', args=(article['article'],)),
                'title': unicode(article['article__title'])
            },
            'rating': article['score']})
    return HttpResponse(json.dumps(hardest_articles),
            content_type='application/json')

@login_required
def api_get_most_clicked_words(request):
    user_id = request.GET.get('user', None)
    num = int(request.GET.get('num', 10))
    period = request.GET.get('period', 'all')
    words = WordHistoryItem.objects.values('word')
    words = filter_on_period(words, period)
    if user_id:
        words = words.filter(user__id=int(user_id))
    if not request.user.is_superuser:
        words = words.filter(user__userprofile__groups__leader=request.user)
    words = words.annotate(score=Count('date')).order_by('-score')
    clicked_words = []
    for word in words.all()[:num]:
        clicked_words.append({
            'word': unicode(word['word']),
            'clicks': word['score']})
    return HttpResponse(json.dumps(clicked_words),
            content_type='application/json')

@login_required
def api_get_viewed_articles(request):
    user_id = request.GET.get('user', None)
    num = int(request.GET.get('num', 10))
    period = request.GET.get('period', 'all')
    history = ArticleHistoryItem.objects
    history = filter_on_period(history, period)
    if user_id:
        history = history.filter(user__id=int(user_id))
    if not request.user.is_superuser:
        history = history.filter(
                user__userprofile__groups__leader=request.user)
    viewed_articles = []
    for view in history.all()[:num]:
        viewed_articles.append({
            'article': {
                'url': reverse('article', args=(view.article.id,)),
                'title': unicode(view.article)
            },
            'date': str(timezone.localtime(view.date))})
    return HttpResponse(json.dumps(viewed_articles),
            content_type='application/json')
