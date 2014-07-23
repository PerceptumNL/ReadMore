from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
import json
import requests

def wiki_request(params):
    """
    Executes query to wikipedia api. Always returns JSON.
    Set global SOURCE_WIKIPEDIA_LANG to change the language.
    """
    if '_lang' in params:
        lang = params['_lang']
        del params['_lang']
    elif hasattr(settings, "SOURCE_WIKIPEDIA_LANG"):
        lang = settings.SOURCE_WIKIPEDIA_LANG
    else:
        lang = 'en'

    params['format'] = 'json'
    url = "http://%s.wikipedia.org/w/api.php" % (lang,)

    r = requests.get(url, params=params)
    return r.json()

def get_portal_url():
    if hasattr(settings, "SOURCE_WIKIPEDIA_LANG"):
        lang = settings.SOURCE_WIKIPEDIA_LANG
    else:
        lang = 'en'

    if lang == 'en':
        return 'Portal:Contents/Portals'

    res = wiki_request({
        '_lang':'en',
        'action':'query',
        'prop':'langlinks',
        'titles':'Portal:Contents/Portals',
        'lllang':lang})

    if 'langlinks' in res['query']['pages']['2533281']:
        return res['query']['pages']['2533281']['langlinks'][0]['*']
    else:
        return None

def extract_title(page):
    title = page.split(":")[1]
    return title.encode('ascii','xmlcharrefreplace')

# Create your views here.
def list_cats(request):
    top = get_portal_url()
    if top is not None:
        res = wiki_request({'action':'parse','prop':'links','page':top})
        if 'links' in res['parse']:
            categories = []
            for link in res['parse']['links']:
                if link['ns'] == 100:
                    categories.append({
                        'id':link['*'],
                        'title':extract_title(link['*'])
                    })
                else:
                    continue
            # TODO: do something with ...
            # http://nl.wikipedia.org/w/api.php?action=parse&prop=sections ...
            # &page=Portaal:Portalenoverzicht
            return HttpResponse(json.dumps(categories),
                content_type='application/json')
        else:
            return HttpResponseNotFound('No topics found in this language.')
    else:
        return HttpResponseNotFound('This language is not supported.')

