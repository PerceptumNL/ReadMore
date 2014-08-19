from django.shortcuts import render
from django.http import HttpResponse
from readmore.content.thirdparty.wiktionary_api import *
import urllib
import json

# Create your views here.
def process(request):
    word = request.GET.get('word',"No word given")
    urlbegin = 'https://nl.wikipedia.org/w/api.php?action=query&titles='
    urlend = '&prop=categories'
    #print urllib.urlopen(urlbegin+'metallica'+urlend).read()
    return HttpResponse(json.dumps({'word':'word'}),
            content_type='application/json')