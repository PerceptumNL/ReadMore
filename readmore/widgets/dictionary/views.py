from django.shortcuts import render
from django.http import HttpResponse
from readmore.content.thirdparty.wiktionary_api import *
import json

# Create your views here.
def process(request):
    word = request.GET.get('word',"No word given")
    api = WiktionaryAPI(languages=['nld'])

    # Get list of Terms and Forms for word
    info = api.get_info(word)

    cards = []
    for term in info:
        card = {}
        if isinstance(term, Term):
            card['type'] = 'DictTermCard'
            card['data'] = {
                'category': term.category_description,
                'word': word,
                'meanings': []
            }
            synonyms = {}
            antonyms = {}
            for index, meaning in enumerate(term.meanings):
                definition = WiktionaryParser.clean_wikitext(
                        meaning.definition)
                example = WiktionaryParser.clean_wikitext(
                        meaning.example)
                card['data']['meanings'].append({
                    'definition': definition,
                    'example': example,
                    'synonyms': meaning.synonyms,
                    'antonyms': meaning.antonyms
                    })
        elif isinstance(term, TermForm):
            card['type'] = 'DictTermCard'
            card['data'] = {
                'category': '',
                'word': word,
                'meanings':
                    [{'definition':t, 'example':''} for t in term.form2text()]
            }
        cards.append(card)
    return HttpResponse(json.dumps(cards).encode('ascii', 'xmlcharrefreplace'),
            content_type='application/json')
