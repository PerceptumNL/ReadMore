import requests
from django.conf import settings

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

def process_title(page):
    title = page.split(":")[1]
    return title.encode('ascii','xmlcharrefreplace')

def get_info(identifier):
    if isinstance(identifier, int) or identifier.isdigit():
        res = wiki_request({
            'action': 'query',
            'prop': 'info',
            'pageids': identifier})
    else:
        res = wiki_request({
            'action': 'query',
            'prop': 'info',
            'titles': identifier})
    info = res['query']['pages'].values()[0]
    if 'missing' in info:
        return None
    else:
        return {'ns': info['ns'], 'title': info['title']}

def get_subcategories(identifier, recursive=False):
    if isinstance(identifier, int) or identifier.isdigit():
        res = wiki_request({
            'action': 'query',
            'list': 'categorymembers',
            'cmpageid': identifier,
            'cmlimit':500,
            'cmnamespace':'14'})
    else:
        res = wiki_request({
            'action': 'query',
            'list': 'categorymembers',
            'cmtitle': identifier,
            'cmlimit':500,
            'cmnamespace':'14'})
    if res != [] and 'categorymembers' in res['query']:
        subcategories = res['query']['categorymembers']
        if recursive:
            for subcategory in subcategories:
                subcategories += get_subcategories(subcategory, True)
    else:
        subcategories = []
    return subcategories

def get_page_links(identifier):
    if isinstance(identifier, int) or identifier.isdigit():
        res = wiki_request({
            'action': 'query',
            'generator': 'links',
            'pageids': identifier,
            'prop': 'info',
            'gpllimit': 500,
            'gplnamespace': 0})
    else:
        res = wiki_request({
            'action': 'query',
            'generator': 'links',
            'titles': identifier,
            'prop': 'info',
            'gpllimit': 500,
            'gplnamespace': 0})
    links = []
    if res != [] and 'pages' in res['query']:
        for link in res['query']['pages'].values():
            if 'missing' in link:
                continue
            links.append({
                'pageid': link['pageid'],
                'title': link['title']})
    return links

def get_page_text(identifier):
    if isinstance(identifier, int) or identifier.isdigit():
        res = wiki_request({
            'action': 'parse',
            'pageid': identifier,
            'prop': 'text'})
    else:
        res = wiki_request({
            'action': 'parse',
            'page': identifier,
            'prop': 'text'})
    if 'parse' in res and 'text' in res['parse']:
        return res['parse']['text']['*']
    else:
        return None
