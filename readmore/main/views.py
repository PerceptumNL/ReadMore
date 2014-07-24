from django.shortcuts import render
from django.http import HttpResponse
from readmore.sources.models import *

# Create your views here.
def home(request):
	categories = Category.objects.all()
	category = Category.objects.filter(pk=2)
	return render(request, 'landing.html', {
		"crtCategory": category,
		"categories": categories,
	})

def categories(request):
	categories = Category.objects.all()
	left_col = categories[0:len(categories)/2]
	right_col = categories[len(categories)/2:len(categories)]
	category = Category.objects.filter(pk=2)
	return render(request, 'categories.html', {
		"crtCategory": category,
		"left": left_col,
		"right": right_col
	})

def category(request, category_id):
    return HttpResponse(category_id)    
