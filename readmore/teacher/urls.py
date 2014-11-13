from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'readmore.teacher.views.dashboard', name='dashboard'),
    url(r'^carddeck/overview/?$', 'readmore.teacher.views.carddeck_overview',
        name='dashboard_carddeck_overview'),
)


