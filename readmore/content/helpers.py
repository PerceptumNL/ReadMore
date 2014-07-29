from django.core.urlresolvers import reverse
from bs4 import BeautifulSoup

def process_wiki_page_html(html):
    """Process the html of a wikipedia page to be used in ReadMore."""
    #TODO: Write BeautifullSoup code to remove Edit links
    #TODO: Write BeautifullSoup code to alter local links,
    #      use: reverse('wikipedia_article', args=(identifier,)) for new link
    #      see also: https://docs.djangoproject.com/en/1.6/ref/urlresolvers/#django.core.urlresolvers.reverse
    soup = BeautifulSoup(html)
    #Find and remove all edit links
    edits = soup.find_all("span", class_="mw-editsection")
    for edit in edits:
    	edit.extract()
    #Find and edit all internal links
    internal = soup.find_all("a")
    for link in internal:
    	source = link.get('href')
    	if source[0:5] == "/wiki":
    		identifier = source[6:]
    		print identifier
    		source = "/content/articles/wikipedia/" + identifier
    		link['href'] = source
    	#print reverse('wikipedia_article', args=(identifier))
    return str(soup)
