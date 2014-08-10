from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'readmore.content.views.barrier', name='barrier'),
    url(r'^index/$', 'readmore.content.views.index', name='home'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^about/', 'readmore.content.views.about', name='about')
)
