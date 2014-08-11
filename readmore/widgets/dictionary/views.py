from django.shortcuts import render
from django.http import HttpResponse
from readmore.content.thirdparty.wiktionary_api import *
import json

# Create your views here.
def process(request):
    word = request.GET.get('word',"No word given")
    print "word: " + str(word)
    api = WiktionaryAPI(languages=['nld'])
    info = api.get_info(word)
    betekenis = []
    print 'inf ' + str(info)
    for i in info:
        bla = i.meanings
        for k in bla:
            print "def: " + str(k.definition)
            betekenis.append(k.definition)
    print betekenis
    return HttpResponse(json.dumps({'word':betekenis}),
            content_type='application/json')
