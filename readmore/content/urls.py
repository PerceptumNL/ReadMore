from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'categories/update/?$',
        'readmore.content.views.update_feeds', name='update_feeds'),
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
    url(r'query/?$', 'readmore.content.views.query', name='content_query'),
    url(r'^search/?$', 'readmore.content.views.searchRelated', name='content_search'),
    )

