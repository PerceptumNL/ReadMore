from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url('r^debug/$', 'main.views.show_technical_report'),
    url(r'^password_reset/$', auth_views.password_reset,
        {'template_name': 'account/password_reset_form.html'},
        name="password_reset"),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'account/password_reset_done.html'},
        name="password_reset_done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'account/password_reset_confirm.html'},
        name="password_reset_confirm"),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'account/password_reset_complete.html'},
        name='password_reset_complete'),
    url(r'^accounts/pilotsignup/$', 'main.views.pilot_signup', name='pilot_signup'),
    url(r'^accounts/profile/$', 'main.views.profile_self', name='profile'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^dashboard/?$', 'main.views.dashboard_dispatch',
        name='dashboard_dispatch'),
    url(r'^profile/(?P<user_id>\w+)$', 'main.views.profile', name='profile'),
    url(r'^add_to_history/$', 'main.views.history', name='history'),
    url(r'^api/group/?$', 'main.views.api_group', name='api_join_group'),
    url(r'^api/stats/total/views/?$',
        'main.views.api_get_total_views',
        name='api_get_total_views'),
    url(r'^api/stats/total/covers/?$',
        'main.views.api_get_total_covers',
        name='api_get_total_covers'),
    url(r'^api/stats/total/ratings/like/?$',
        'main.views.api_get_total_like_ratings',
        name='api_get_total_like_ratings'),
    url(r'^api/stats/total/ratings/difficulty/?$',
        'main.views.api_get_total_difficulty_ratings',
        name='api_get_total_difficulty_ratings'),
    url(r'^api/list/events/last/?$',
        'main.views.api_get_last_events',
        name='api_get_last_events'),
    url(r'^api/list/users/active/?$',
        'main.views.api_get_most_active_users',
        name='api_get_most_active_users'),
    url(r'^api/list/articles/hardest/?$',
        'main.views.api_get_hardest_articles',
        name='api_get_hardest_articles'),
    url(r'^api/list/articles/favorite/?$',
        'main.views.api_get_favorite_articles',
        name='api_get_favorite_articles'),
    url(r'^api/list/articles/viewed/?$',
        'main.views.api_get_viewed_articles',
        name='api_get_viewed_articles'),
    url(r'^api/list/words/clicked/?$',
        'main.views.api_get_most_clicked_words',
        name='api_get_most_clicked_words'),
)
