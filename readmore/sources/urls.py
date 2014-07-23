from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'wikipedia/cat/?$', 'readmore.sources.wikipedia.views.list_cats'))
