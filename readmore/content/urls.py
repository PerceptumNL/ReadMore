from django.conf.urls import patterns, include, url

"""
Retrieve main categories
/sources/
Retrieve articles and subcategories in Category 1
/sources/?category=1
Retrieve Article Lijst_van_sporten from wikipedia source
/sources/wikipedia/Lijst_van_sporten
"""

urlpatterns = patterns('',
    url(r'wikipedia/(?P<identifier>.+)$',
        'readmore.sources.views.wiki_article', name='source_wiki_article'),
    url(r'readmore/(?P<identifier>\d+)$',
        'readmore.sources.views.article', name='source_article'),
    url(r'$', 'readmore.sources.views.index', name='source_index'))

