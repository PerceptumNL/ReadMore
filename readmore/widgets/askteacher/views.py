from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
def process(request):
    cards = [{'type':'FormCard', 'data': {'title': 'Vraag aan de docent'}}]
    return HttpResponse(json.dumps(cards).encode('ascii', 'xmlcharrefreplace'),
            content_type='application/json')
