from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'readmore.teacher.views.dashboard', name='dashboard'),
)


