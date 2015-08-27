from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'content.views.overview', name='article_overview'),
    url(r'categories/update/?$',
        'content.views.update_feeds', name='update_feeds'),
    url(r'articles/(?P<identifier>\d+)$',
        'content.views.article', {'source':'local'},
        name='article'),
    url(r'articles/wikipedia/(?P<identifier>.+)$',
        'content.views.article', {'source':'wikipedia'},
        name='wikipedia_article'),
    url(r'categories/(?P<identifier>\d+)$',
        'content.views.category', {'source':'local'},
        name='category'),
    url(r'categories/wikipedia/(?P<identifier>.+)$',
        'content.views.category', {'source':'wikipedia'},
        name='wikipedia_category'),
    url(r'query/?$', 'content.views.query', name='content_query'),
    )

