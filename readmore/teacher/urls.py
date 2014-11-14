from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'readmore.teacher.views.dashboard', name='dashboard'),
    url(r'^carddeck/overview/?$', 'readmore.teacher.views.carddeck_overview',
        name='dashboard_carddeck_overview'),
    url(r'^carddeck/user/?$', 'readmore.teacher.views.carddeck_user',
        name='dashboard_carddeck_user'),
    url(r'^carddeck/article/?$', 'readmore.teacher.views.carddeck_article',
        name='dashboard_carddeck_article'),
    url(r'^carddeck/word/?$', 'readmore.teacher.views.carddeck_word',
        name='dashboard_carddeck_word'),
)


