from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'readmore.content.views.index', name='home'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/(?P<user_id>\w+)$', 'readmore.main.views.profile', name='profile'),
    url(r'^about/', 'readmore.content.views.about', name='about')
)
