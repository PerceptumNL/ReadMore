from django.core.urlresolvers import reverse
from bs4 import BeautifulSoup

def process_wiki_page_html(html):
    """Process the html of a wikipedia page to be used in ReadMore."""
    #TODO: Write BeautifullSoup code to remove Edit links
    #TODO: Write BeautifullSoup code to alter local links,
    #      use: reverse('wikipedia_article', args=(identifier,)) for new link
    #      see also: https://docs.djangoproject.com/en/1.6/ref/urlresolvers/#django.core.urlresolvers.reverse
    return html
