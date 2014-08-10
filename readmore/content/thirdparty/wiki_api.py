"""Wikipedia API module."""

import requests
from django.conf import settings

# Define constants of the three used wikipedia namespaces
# See http://meta.wikimedia.org/wiki/Help:Namespace for more information.
NS_PAGE = '0'
NS_CATEGORY = '14'
NS_PORTAL = '100'

def process_title(title):
    """Chop-off the first term before the ':'."""
    title = title.split(":")[1]
    return title.encode('ascii', 'xmlcharrefreplace')


class MediaWikiAPI(object):
    _lang = u''
    _base_url = u''

    def __init__(self, lang=None, base_url=None):
        if lang is not None:
            self._lang = lang
        elif hasattr(settings, "CONTENT_MEDIAWIKI_LANG"):
            self._lang = settings.CONTENT_MEDIAWIKI_LANG
        else:
            self._lang = 'en'

        if base_url is not None:
            self._base_url = base_url
        elif hasattr(settings, "CONTENT_MEDIAWIKI_API_URL"):
            self._base_url = settings.CONTENT_MEDIAWIKI_API_URL
        else:
            self._base_url = 'http://%s.wikipedia.org/w/api.php'

    def _request(self, params):
        """
        Executes query to wikipedia api. Always returns JSON.
        Set global SOURCE_WIKIPEDIA_LANG to change the language.
        """
        if '_lang' in params:
            lang = params['_lang']
            del params['_lang']
        else:
            lang = self._lang

        params['format'] = 'json'
        try:
            url = self._base_url % (lang,)
        except TypeError:
            url = self._base_url

        print url, params

        res = requests.get(url, params=params)
        return res.json()

    def get_portal_url(self):
        if self._lang == 'en':
            return 'Portal:Contents/Portals'

        res = self._request({
            '_lang':'en',
            'action':'query',
            'prop':'langlinks',
            'titles':'Portal:Contents/Portals',
            'lllang':self._lang})

        try:
            return res['query']['pages']['2533281']['langlinks'][0]['*']
        except KeyError:
            return None

    def get_info(self, identifier):
        if isinstance(identifier, int):
            res = self._request({
                'action': 'query',
                'prop': 'info',
                'pageids': identifier})
        else:
            res = self._request({
                'action': 'query',
                'prop': 'info',
                'titles': identifier})
        info = res['query']['pages'].values()[0]
        if 'missing' in info:
            return None
        else:
            return {'ns': info['ns'], 'title': info['title']}

    def get_page_extract(self, identifier, chars=100):
        if isinstance(identifier, int):
            res = self._request({
                'action': 'query',
                'pageids': identifier,
                'prop': 'extracts',
                'exchars': chars})
        else:
            res = self._request({
                'action': 'query',
                'titles': identifier,
                'prop': 'extracts',
                'exchars': chars})
        info = res['query']['pages'].values()[0]
        if 'missing' in info:
            return None
        else:
            return info['extract']

    def get_category_members(self, identifier, namespace=NS_CATEGORY,
            recursive=False):
        if isinstance(identifier, int):
            res = self._request({
                'action': 'query',
                'list': 'categorymembers',
                'cmpageid': identifier,
                'cmlimit':500,
                'cmnamespace':namespace})
        else:
            res = self._request({
                'action': 'query',
                'list': 'categorymembers',
                'cmtitle': identifier,
                'cmlimit':500,
                'cmnamespace':namespace})
        if res != [] and 'categorymembers' in res['query']:
            members = res['query']['categorymembers']
            if recursive:
                for member in members:
                    members += self.get_category_members(
                            member, namespace, True)
        else:
            members = []
        return members

    def get_page_links(self, identifier):
        if isinstance(identifier, int):
            res = self._request({
                'action': 'query',
                'generator': 'links',
                'pageids': identifier,
                'prop': 'info',
                'gpllimit': 500,
                'gplnamespace': NS_PAGE})
        else:
            res = self._request({
                'action': 'query',
                'generator': 'links',
                'titles': identifier,
                'prop': 'info',
                'gpllimit': 500,
                'gplnamespace': NS_PAGE})
        links = []
        if res != [] and 'pages' in res['query']:
            for link in res['query']['pages'].values():
                if 'missing' in link:
                    continue
                links.append({
                    'pageid': link['pageid'],
                    'title': link['title']})
        return links

    def get_page_text(self, identifier):
        if isinstance(identifier, int):
            res = self._request({
                'action': 'parse',
                'pageid': identifier,
                'prop': 'text'})
        else:
            res = self._request({
                'action': 'parse',
                'page': identifier,
                'prop': 'text'})
        try:
            return res['parse']['text']['*']
        except KeyError:
            return None

    def get_page_wikitext(self, identifier):
        if isinstance(identifier, int):
            res = self._request({
                'action': 'query',
                'pageids': identifier,
                'prop': 'revisions',
                'rvprop': 'content'})
        else:
            res = self._request({
                'action': 'query',
                'titles': identifier,
                'prop': 'revisions',
                'rvprop': 'content'})
        try:
            return res['query']['pages'].values()[0]['revisions'][0]['*']
        except KeyError:
            return None
