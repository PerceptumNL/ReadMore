from django.shortcuts import render
from django.http import HttpResponse

def carddeck(request):
    return render(request, 'carddeck.html', {})
