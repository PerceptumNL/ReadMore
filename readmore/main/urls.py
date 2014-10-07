from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'readmore.main.views.login', name='login'),
    url(r'^$', 'readmore.content.views.index', name='home'),
    url(r'^articleNew$', 'readmore.main.views.articleNew', name='article'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/profile/$', 'readmore.main.views.profileSelf', name='profile'), 
    url(r'^accounts/login/$', 'readmore.main.views.login', name='login2'),
    url(r'^accounts/signup/$', 'readmore.main.views.login', name='login3'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/(?P<user_id>\w+)$', 'readmore.main.views.profile', name='profile'),
    url(r'^about/', 'readmore.content.views.about', name='about')
)
