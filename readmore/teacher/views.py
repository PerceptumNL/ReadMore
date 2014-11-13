from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import json

# Create your views here.
@login_required
def dashboard(request):
    # If user is teacher
    if True:
    
    
    
        return render(request, 'teacher/dashboard.html', {
        
        })
    else:
        return HttpResponseRedirect("/")


@login_required
def carddeck_overview(request):
    return HttpResponse(json.dumps([
        {
            'type': 'DashboardTotalCard',
            'data': {
                'title': 'Artikelen bekeken',
                'source': reverse('api_get_total_views')
            }
        },
        {
            'type': 'DashboardTotalCard',
            'data': {
                'title': 'Woorden bekeken',
                'source': reverse('api_get_total_covers')
            }
        }]), content_type='application/json')
