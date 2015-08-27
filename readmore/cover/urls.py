from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'dictionary/?$', dictionary,
        name='widget_dictionary'),
    url(r'customcard/?$', custom_card,
        name='widget_customcard'))

