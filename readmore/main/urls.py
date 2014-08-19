from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'readmore.content.views.index', name='home'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
<<<<<<< HEAD
    url(r'^profile/(?P<user_id>\w+)$', 'readmore.main.views.profile', name='profile'),
=======
    url(r'^about/', 'readmore.content.views.about', name='about')
>>>>>>> e30c0fb0109fbe52066462e1e55521edfdfe6746
)
