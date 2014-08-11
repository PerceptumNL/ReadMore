from django.shortcuts import render
from django.http import HttpResponse
from readmore.content.thirdparty.wiktionary_api import *
import json

# Create your views here.
def process(request):
    print "hi"
    word = request.GET.get('word',"No word given")
    return HttpResponse(json.dumps({'word':word}),
            content_type='application/json')
