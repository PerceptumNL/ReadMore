from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'readmore.content.views.index', name='home'),
        url(r'^accounts/', include('allauth.urls')),
)
