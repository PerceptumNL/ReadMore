from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):
    # If user is teacher
    if True:
    
    
    
        return render(request, 'teacher/dashboard.html', {
        
        })
    else:
        return HttpResponseRedirect("/")
