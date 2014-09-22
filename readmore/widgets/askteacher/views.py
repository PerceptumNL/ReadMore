from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
import json

# Create your views here.
def process(request):
    if request.method == "POST":
        pass
    elif request.method == "GET":
        cards = [{'type':'FormCard', 'data': {'title': 'Vraag aan de docent'}}]
        return HttpResponse(json.dumps(cards).encode('ascii', 'xmlcharrefreplace'),
                content_type='application/json')
    else:
        return HttpResponseBadRequest()

