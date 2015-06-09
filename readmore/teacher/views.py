from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from readmore.main.models import *
from readmore.content.models import *
from readmore.widgets.customcard.models import CustomCard
from django.utils.translation import ugettext as _
from datetime import datetime, timedelta
from collections import Counter
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
import math
import helpers
import json

@login_required
def dashboard_test(request):
    if request.user.is_superuser or len(Group.objects.filter(leader=request.user)):
        groups = Group.objects.filter(leader=request.user)
        articles = RSSArticle.objects.filter(publication_date__gte=datetime.now()-timedelta(days=7))
        return render(request, 'teacher/dashboard/main.html', {
        "groups": groups,        
    })
    else:
        return HttpResponseRedirect("/")
        
def dashboard_group(request, group_id=None):
    if request.user.is_superuser or len(Group.objects.filter(leader=request.user)):
        group = Group.objects.get(pk=group_id)
        students = User.objects.filter(userprofile__groups__pk__in=group_id)

        return render(request, 'teacher/dashboard/group.html', {
            "group": group,
            "students": students,
    })
    else:
        return HttpResponseRedirect("/")
        
def dashboard_student(request, group_id=None, student_id=None):
    if request.user.is_superuser or len(Group.objects.filter(leader=request.user)):
        student = User.objects.get(pk=student_id)
        group = Group.objects.get(pk=group_id)
        return render(request, 'teacher/dashboard/student.html', {
            "group": group,
            "student": student,
    })
    else:
        return HttpResponseRedirect("/")


@login_required
def api_group(request, group_id=None):
    """API for group statistics.
    Request args:
        filter: Determines what statistics are included
            0 = all
            1 = student count, article read, article word, engagement, articles, words
            2 = top 3 categories"""
    filter = int(request.GET.get('filter',0))
    result_dict = {}
    
    if filter < 2:
        students = User.objects.filter(userprofile__groups__pk__in=group_id)
        student_count = len(students)
        if student_count > 0:
            article_read = {"week": 0, "month": 0, "total": 0}
            article_word = {"week": 0, "month": 0, "total": 0}
            engagement = 0
            articles = []
            words = []
        
            article_read = api_get_history_totals(ArticleHistoryItem.objects, group_id)
            article_word = api_get_history_totals(WordHistoryItem.objects, group_id)

            art_per_stud = article_read["week"]/float(student_count)
            engagement_norm = art_per_stud/2.0
            engagement = int(min(5, math.floor(engagement_norm*5)))

            article_his = ArticleHistoryItem.objects.filter(user__userprofile__groups__in=group_id)
            article_his = filter_on_period(article_his, 'week')
            article_pks = article_his.values_list('article__pk', flat=True)
            article_pks = sorted(article_pks, key=Counter(article_pks).get, reverse=True)
            seen = set()
            article_pks_f = [x for x in article_pks if x not in seen and not seen.add(x)]
            freqs = Counter(article_pks)
            for pk in article_pks_f:
                article = Article.objects.get(pk=pk)
                articles.append( {
                    'title': article.title,
                    'image': article.image,
                    'pk': article.pk,
                    'url': reverse('article', kwargs={'identifier': article.pk}),
                    'freq': freqs[pk]
                    })
            articles = articles[:10]

            word_his = WordHistoryItem.objects.filter(user__userprofile__groups__in=group_id)
            word_his = filter_on_period(word_his, 'week')
            words = list(set(word_his.values_list('word', flat=True)))
            
            result_dict["student_count"] = student_count
            result_dict["article_read"] = article_read
            result_dict["article_word"] = article_word
            result_dict["engagement"] = engagement
            result_dict["articles"] = articles
            result_dict["words"] = sorted(words)
        
    if filter in (0, 2):
        counts = group_category_counts(group_id)
        categories = sorted(counts, key=counts.get)[:3]
        
        result_dict["categories"] = categories
    
    return HttpResponse(json.dumps(result_dict), content_type='application/json')

@login_required
def api_student(request, student_id=None):
    """API for student statistics.
    Request args:
        filter: Determines what statistics are included
            0 = all
            1 = article counts, engagement
            2 = words clicked, articles read, ratings, average read count"""
    filter = int(request.GET.get('filter',0))
    result_dict = {}
    
    article_history = ArticleHistoryItem.objects.filter(user__pk=student_id)
    article_counts = student_article_count(article_history)
    
    if filter < 2:
        engagement = 0

        """ A temporary definition of engagement. Conferred with David and the ideal
        definition would be based on the "actually" read article count related to the
        estimated capacity of the student, e.g. not punish students for being slower
        than the rest of the group. Additionally a good measure would be any
        interaction with the platform, such as ratings, word clicks, etc."""
        engagement = int(min(5, article_counts["week"]))
        
        result_dict["article_counts"] = article_counts
        result_dict["engagement"] = engagement
    
    if filter in (0, 2):
        """Still learning
        try:
            student = User.objects.get(userprofile__pk=student_id)
        except ObjectDoesNotExist:
            print "Invalid student ID"
        clicked = student.wordhistoryitem_set.all()"""
        clicked_words = unique_strs(WordHistoryItem.objects.filter(user__pk=student_id))
        
        articles_read = unique_strs(article_history)
        
        ratings = ArticleRatingItem.objects.filter(user__pk=student_id)
        
        result_dict["clicked_words"] = clicked_words
        result_dict["articles_read"] = articles_read
        
    return HttpResponse(json.dumps(result_dict), content_type='application/json')

def group_category_counts(group_id):
    history = ArticleHistoryItem.objects.filter(user__userprofile__groups=group_id)
    counts = {}
    for category in Category.objects.all():
        category_articles = history.filter(article__categories=category)
        counts[category.title] = len(category_articles)

    return counts
    
def student_article_count(history):
    total_all = filter_on_period(history, 'total').count()
    total_month = filter_on_period(history, 'month').count()
    total_week = filter_on_period(history, 'week').count()
    return {
        'week': total_week,
        'month': total_month,
        'total': total_all
    }

def unique_strs(objs):
    return list(set([unicode(obj) for obj in objs]))
    
def filter_on_period(objects, period):
    if period == 'month':
        date = datetime.now(pytz.utc)
        return objects.filter(date__month=date.month)
    elif period == 'week':
        date = datetime.now(pytz.utc)
        date -= timedelta(hours=date.hour)
        date -= timedelta(minutes=date.minute)
        date -= timedelta(seconds=date.second)
        date -= timedelta(microseconds=date.microsecond)
        start_week = date - timedelta(date.weekday())
        end_week = start_week + timedelta(7)
        return objects.filter(date__range=[start_week, end_week])
    else:
        return objects

def api_get_history_totals(history, group_id):
    history = history.filter(user__userprofile__groups__in=group_id)
    total_all = filter_on_period(history, 'total').count()
    total_month = filter_on_period(history, 'month').count()
    total_week = filter_on_period(history, 'week').count()
    return {
            'week': total_week,
            'month': total_month,
            'total': total_all
        }

def api_group_read(request, group_id=None):
    pass
def api_group_words(request, group_id=None):
    pass
def api_group_engaged(request, group_id=None):
    pass
def api_group_mostread(request, group_id=None):
    pass

# Create your views here.
@login_required
def overview(request):
    if request.user.is_superuser or len(Group.objects.filter(leader=request.user)):
        return render(request, 'teacher/overview.html',)
    else:
        return HttpResponseRedirect("/")

@login_required
def add_user(request):
    group_list = Group.objects.filter(leader=request.user)
    message = ""
    if request.user.is_superuser or len(group_list):
        if(request.method=="POST"):
            username = request.POST.get('username', None)
            email = request.POST.get('email', None)
            group = request.POST.get('group', None)
            if len(User.objects.filter(username=username)) == 0:
                password = helpers.generate_password()
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.save()
                new_profile = UserProfile(user=new_user)
                new_profile.save()
                group_choice = Group.objects.get(pk=group)
                new_profile.groups.add(group)
                new_profile.save()
                message = "Nieuwe gebruiker '" + str(username) + "' aangemaakt met wachtwoord " + str(password) + ", in groep " + str(group_choice.title) + " van instituut " + str(group_choice.institute)
            else:
                message = "Gebruiker '" + str(username) + "' bestaat al, gebruik alstublieft een andere naam."
        return render(request, 'teacher/manage_users.html', {
            'message':message,
            'groups':group_list,
            })

@login_required
def manage_users(request):
    group_list = Group.objects.filter(leader=request.user)
    if request.user.is_superuser or len(group_list):

        return render(request, 'teacher/manage_users.html',
            {
            'groups': group_list,
            })
    else:
        return HttpResponseRedirect("/")

@login_required
def dashboard(request):
    if request.user.is_superuser:
        user_list = User.objects.all()
    else:
        user_list = User.objects.filter(userprofile__groups__leader=request.user)
    if len(Group.objects.filter(leader=request.user)):
        return render(request, 'teacher/dashboard.html', {
            'users': user_list,
        })
    else:
        return HttpResponseRedirect("/")

@login_required
def word_cards(request):
    cards = CustomCard.objects.all()
    return render(request, 'teacher/teachercards.html', {
        "word_cards": cards
    })

@login_required
def add_word(request):
    if request.method == "GET":
        return render(request, 'teacher/teachercard.html')
    if request.method == 'POST':
        word = request.POST.get('word', None)
        description = request.POST.get('description', None)
        if len(word)==0:
            word=None
        if len(description)==0:
            description=None
        if word is not None and description is not None :
            try:
                CustomCard.objects.create(word=word, content=description, user=request.user)
                return HttpResponseRedirect("woordkaarten")
            except Exception as e:
                # Bad request
                return HttpResponse(status=404)
    # Not a post request

@login_required
def remove_word(request):
    if request.method == 'POST':
        word_pk = request.POST.get('word', None)
        if word_pk is not None :
            try:
                card = CustomCard.objects.get(pk=word_pk)
                card.delete()
                return HttpResponseRedirect("woordkaarten")
            except Exception as e:
                # Bad request
                return HttpResponse(status=404)
    # Not a post request
    return HttpResponseRedirect("woordkaarten")

@login_required
def retrieve_students(request):
    users = [{'label': _('Everybody'), 'id': ''}]
    if request.user.is_superuser:
        user_list = User.objects.all()
    else:
        user_list = User.objects.filter(userprofile__groups__leader=request.user)
    displayname = (lambda user: u' '.join([user.first_name, user.last_name])
            if user.first_name else user.username)
    users += sorted(
            [{'label': displayname(user), 'id': user.pk} for user in user_list],
            key=lambda x: x['label'])
    return HttpResponse(json.dumps(users), content_type='application/json')

@login_required
def carddeck_overview(request):
    return HttpResponse(json.dumps([
        {
            'type': 'dashboard-list-events-card',
            'data': {
                'title': 'Laatste gebeurtenissen',
                'description':
                    "Overzicht van de laatste acties op het platform.",
                'source': reverse('api_get_last_events')
            }
        },
        {
            'type': 'dashboard-list-user-number',
            'data': {
                'title': 'Meest actieve leerlingen',
                'description':
                    "Overzicht van de meest actieve leerlingen.",
                'source': reverse('api_get_most_active_users')
            }
        },
        {
            'type': 'dashboard-list-word-number',
            'data': {
                'title': 'Meest bekeken woorden',
                'description':
                    "Overzicht van de meest bekeken woorden.",
                'source': reverse('api_get_most_clicked_words')
            }
        },
        {
            'type': 'dashboard-list-articles',
            'data': {
                'title': 'Bekeken artikelen',
                'description':
                    "Overzicht van de bekeken artikelen.",
                'source': reverse('api_get_viewed_articles')
            }
        },
        {
            'type': 'dashboard-list-article-stars',
            'data': {
                'title': 'Moeilijkste artikelen',
                'description':
                    "Overzicht van de moeilijkste artikelen.",
                'source': reverse('api_get_hardest_articles')
            }
        },
        {
            'type': 'dashboard-list-article-stars',
            'data': {
                'title': 'Favoriete artikelen',
                'description':
                    "Overzicht van de meest favoriete artikelen.",
                'source': reverse('api_get_favorite_articles')
            }
        },
        {
            'type': 'dashboard-total-card',
            'data': {
                'title': 'Artikelen bekeken',
                'description': (
                    "Totaal aantal bekeken artikelen in een "
                    "bepaalde periode."),
                'source': reverse('api_get_total_views')
            }
        },
        {
            'type': 'dashboard-total-card',
            'data': {
                'title': 'Woorden bekeken',
                'description': (
                    "Totaal aantal geklikte woorden in een "
                    "bepaalde periode."),
                'source': reverse('api_get_total_covers')
            }
        },
        {
            'type': 'dashboard-total-card',
            'data': {
                'title': 'Moeilijkheid aangegeven',
                'description': (
                    "Totaal aantal keer dat de moeilijkheid "
                    "van een artikel is aangegeven in een "
                    "bepaalde periode."),
                'source': reverse('api_get_total_difficulty_ratings')
            }
        },
        {
            'type': 'dashboard-total-card',
            'data': {
                'title': 'Interessantheid aangegeven',
                'description': (
                    "Totaal aantal keer dat de interessantheid "
                    "van een artikel is aangegeven in een "
                    "bepaalde periode."),
                'source': reverse('api_get_total_like_ratings')
            }
        }]), content_type='application/json')

@login_required
def carddeck_user(request):
    return HttpResponse(json.dumps([
        {
            'type': 'dashboard-list-events-card',
            'data': {
                'title': 'Laatste gebeurtenissen',
                'description':
                    "Overzicht van de laatste acties op het platform.",
                'source': reverse('api_get_last_events')
            }
        },
        {
            'type': 'dashboard-list-word-number',
            'data': {
                'title': 'Meest bekeken woorden',
                'description':
                    "Overzicht van de meest bekeken woorden.",
                'source': reverse('api_get_most_clicked_words')
            }
        },
        {
            'type': 'dashboard-list-articles',
            'data': {
                'title': 'Bekeken artikelen',
                'description':
                    "Overzicht van de bekeken artikelen.",
                'source': reverse('api_get_viewed_articles')
            }
        },
        {
            'type': 'dashboard-list-article-stars',
            'data': {
                'title': 'Moeilijkste artikelen',
                'description':
                    "Overzicht van de moeilijkste artikelen.",
                'source': reverse('api_get_hardest_articles')
            }
        },
        {
            'type': 'dashboard-list-article-stars',
            'data': {
                'title': 'Favoriete artikelen',
                'description':
                    "Overzicht van de meest favoriete artikelen.",
                'source': reverse('api_get_favorite_articles')
            }
        },
        {
            'type': 'dashboard-total-card',
            'data': {
                'title': 'Artikelen bekeken',
                'description': (
                    "Totaal aantal bekeken artikelen in een "
                    "bepaalde periode."),
                'source': reverse('api_get_total_views')
            }
        },
        {
            'type': 'dashboard-total-card',
            'data': {
                'title': 'Woorden bekeken',
                'description': (
                    "Totaal aantal geklikte woorden in een "
                    "bepaalde periode."),
                'source': reverse('api_get_total_covers')
            }
        },
        {
            'type': 'dashboard-total-card',
            'data': {
                'title': 'Moeilijkheid aangegeven',
                'description': (
                    "Totaal aantal keer dat de moeilijkheid "
                    "van een artikel is aangegeven in een "
                    "bepaalde periode."),
                'source': reverse('api_get_total_difficulty_ratings')
            }
        },
        {
            'type': 'dashboard-total-card',
            'data': {
                'title': 'Interessantheid aangegeven',
                'description': (
                    "Totaal aantal keer dat de interessantheid "
                    "van een artikel is aangegeven in een "
                    "bepaalde periode."),
                'source': reverse('api_get_total_like_ratings')
            }
        }]), content_type='application/json')

@login_required
def carddeck_article(request):
    return HttpResponse(json.dumps([
        {
            'type': 'dashboard-list-articles',
            'data': {
                'title': 'Bekeken artikelen',
                'description':
                    "Overzicht van de bekeken artikelen.",
                'source': reverse('api_get_viewed_articles')
            }
        },
        {
            'type': 'dashboard-list-article-stars',
            'data': {
                'title': 'Moeilijkste artikelen',
                'description':
                    "Overzicht van de moeilijkste artikelen.",
                'source': reverse('api_get_hardest_articles')
            }
        },
        {
            'type': 'dashboard-list-article-stars',
            'data': {
                'title': 'Favoriete artikelen',
                'description':
                    "Overzicht van de meest favoriete artikelen.",
                'source': reverse('api_get_favorite_articles')
            }
        },
        {
            'type': 'dashboard-total-card',
            'data': {
                'title': 'Artikelen bekeken',
                'description': (
                    "Totaal aantal bekeken artikelen in een "
                    "bepaalde periode."),
                'source': reverse('api_get_total_views')
            }
        }]), content_type='application/json')

@login_required
def carddeck_word(request):
    return HttpResponse(json.dumps([
        {
            'type': 'dashboard-list-word-number',
            'data': {
                'title': 'Meest bekeken woorden',
                'description':
                    "Overzicht van de meest bekeken woorden.",
                'source': reverse('api_get_most_clicked_words')
            }
        }]), content_type='application/json')
