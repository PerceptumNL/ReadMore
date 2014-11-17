from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomCard
from django.utils.translation import ugettext as _
import json

# Create your views here.
def process(request):
    word = request.GET.get('word',"No word given")
    cards = []
    for card in CustomCard.objects.filter(word=word):
        cards.append({
            'type': 'CustomCard',
            'data': {
                'content': card.content,
                'title': _("Message from %s") % (card.user,)
            }
        })
    return HttpResponse(json.dumps(cards).encode('ascii', 'xmlcharrefreplace'),
            content_type='application/json')
