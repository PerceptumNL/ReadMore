from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'base.html', {
        "crtCategory": {"name": "test", "pk": 0},
        "categories": [{"name": "test", "pk": 0},{"name": "test2", "pk": 1}]
       
    })

def categories(request):
    return HttpResponse("ReadMore")

def category(request, category_id):
    return HttpResponse(category_id)    
