from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^accounts/profile/$', 'readmore.main.views.profile_self', name='profile'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', 'readmore.main.views.article_overview', name='article_overview'),
    url(r'^profile/(?P<user_id>\w+)$', 'readmore.main.views.profile', name='profile'),
    url(r'^about/', 'readmore.main.views.about', name='about'),
    url(r'^add_to_history/$', 'readmore.main.views.history', name='history'),
)


