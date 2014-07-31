from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
def process(request):
    word = request.GET.get('word',"No word given")
    return HttpResponse(json.dumps({'word':word}),
            content_type='application/json')
