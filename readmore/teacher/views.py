from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from readmore.main.models import Group
import json

# Create your views here.
@login_required
def dashboard(request):
    # If user is teacher
    user_list = User.objects.all()
    if True:
        return render(request, 'teacher/dashboard.html', {
            'users': user_list,
        })
    else:
        return HttpResponseRedirect("/")

@login_required
def retrieve_students(request):
    user_list = []
    for group in Group.objects.filter(leader__id=request.user.id):
        user_list += [profile.user for profile in group.users.all()]
    user_list.append(request.user)
    users = [{'label': user.username, 'id': user.pk} for user in user_list]
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
