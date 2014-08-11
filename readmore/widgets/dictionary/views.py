from django.shortcuts import render
from django.http import HttpResponse
from readmore.content.thirdparty.wiktionary_api import *
import json

# Create your views here.
def process(request):
    word = request.GET.get('word',"No word given")
    print "word: " + str(word)
    api = WiktionaryAPI(languages=['nld'])
    #mainterm = api.get_info(word)[0].main_term
    #print "main: " + str(mainterm)
    info = api.get_info(word)
    betekenis = [str(word) + " >> " + str(word)]
    betekenis.append('<ul>')
    print 'inf ' + str(info)
    for meaninglist in info:
        allmeanings = meaninglist.meanings
        for singlemeaning in allmeanings:
            betekenis.append('<li>' + singlemeaning.definition + '</li>')
    betekenis.append('</ul>')
    print betekenis
    return HttpResponse(json.dumps({'word':betekenis}),
            content_type='application/json')
