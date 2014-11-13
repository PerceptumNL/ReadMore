from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^accounts/profile/$', 'readmore.main.views.profile_self', name='profile'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', 'readmore.main.views.article_overview', name='article_overview'),
    url(r'^profile/(?P<user_id>\w+)$', 'readmore.main.views.profile', name='profile'),
    url(r'^about/', 'readmore.main.views.about', name='about'),
    url(r'^add_to_history/$', 'readmore.main.views.history', name='history'),
    url(r'^api/stats/total/views/?$',
        'readmore.main.views.api_get_total_views',
        name='api_get_total_views'),
    url(r'^api/stats/total/views/(?P<user_id>[0-9]+)/?$',
        'readmore.main.views.api_get_total_views',
        name='api_get_total_views'),
    url(r'^api/stats/total/covers/?$',
        'readmore.main.views.api_get_total_covers',
        name='api_get_total_covers'),
    url(r'^api/stats/total/covers/(?P<user_id>[0-9]+)/?$',
        'readmore.main.views.api_get_total_covers',
        name='api_get_total_covers'),
)


