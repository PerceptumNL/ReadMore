from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'articles/(?P<identifier>\d+)$',
        'readmore.content.views.article', {'source':'local'},
        name='article'),
    url(r'articles/wikipedia/(?P<identifier>.+)$',
        'readmore.content.views.article', {'source':'wikipedia'},
        name='wikipedia_article'),
    url(r'categories/(?P<identifier>\d+)$',
        'readmore.content.views.category', {'source':'local'},
        name='category'),
    url(r'categories/wikipedia/(?P<identifier>.+)$',
        'readmore.content.views.category', {'source':'wikipedia'},
        name='wikipedia_category'),
    url(r'$', 'readmore.content.views.index', name='content_index'))
