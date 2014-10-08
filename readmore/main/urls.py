from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'readmore.content.views.index', name='home'),
    url(r'^accounts/profile/$', 'readmore.main.views.profile_self', name='profile'),
    url(r'^accounts/login/$', 'readmore.main.views.login', name='login'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/(?P<user_id>\w+)$', 'readmore.main.views.profile', name='profile'),
    url(r'^about/', 'readmore.main.views.about', name='about')
)
