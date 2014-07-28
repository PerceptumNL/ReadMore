from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'readmore.sources.views.index', name='home'),
    url(r'^categories/$', 'readmore.main.views.categories', name='categories'),
    url(r'^category/(?P<category_id>\d+)/?$', 'readmore.main.views.category', name='category'),
    url(r'^navigation/?$', 'readmore.sources.views.index', name='navigation'),
)
