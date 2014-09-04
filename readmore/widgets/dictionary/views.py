from django.shortcuts import render
from django.http import HttpResponse
from readmore.content.thirdparty.wiktionary_api import *
import json

# Create your views here.
def process(request):
    return HttpResponse(json.dumps([{"data": {"term_category": "noun", "synonyms": {"0": ["canape", "divan", "sofa"], "2": ["zandbank"]}, "word": "bank"}, "type": "DictSynonymCard"}, {"data": {"category": "noun", "meanings": {"0": {"definition": "een meubelstuk met zitplaats voor meer dan een persoon", "example": "Ze zaten op de '''bank''' naar de tv te kijken."}, "1": {"definition": "een financiele instelling", "example": "Vader was naar de '''bank''' om te praten over een lening."}, "2": {"definition": "een ondiepte in het water", "example": "De boot was op een '''bank''' vastgelopen."}, "3": {"definition": "gebouw waarin een financiele instelling gevestigd is", "example": ""}, "4": {"definition": "een opslagsysteem voor gegevens of voorwerpen b.v. beeldbank, bloedbank, boekenbank, kennisbank, spermabank", "example": ""}, "5": {"definition": "harde aardlaag", "example": ""}, "6": {"definition": "donkere laag of streep van wolken aan de horizon.", "example": ""}, "7": {"definition": "werktafel b.v. draaibank etc.", "example": ""}}, "word": "bank"}, "type": "DictTermCard"}, {"data":{"antonyms":{"1":["honesty", "trust"]}, "word":"bank", "term_category":"noun"}, "type": "DictAntonymCard"}]), content_type='application/json')
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
                'meanings': {}
            }
            synonyms = {}
            antonyms = {}
            for index, meaning in enumerate(term.meanings):
                definition = WiktionaryParser.clean_wikitext(
                        meaning.definition)
                example = WiktionaryParser.clean_wikitext(
                        meaning.example)
                card['data']['meanings'][index] = {
                    'definition': definition,
                    'example': example}
                if meaning.synonyms:
                    synonyms[index] = meaning.synonyms
                if meaning.antonyms:
                    antonyms[index] = meaning.antonyms
            # Create corresponding synonyms card
            cards.append({'type': 'DictSynonymCard',
                'data': {
                    'word': word,
                    'term_category': card['data']['category'],
                    'synonyms': synonyms}})
            # Create corresponding synonyms card
            cards.append({'type': 'DictAntonymCard',
                'data': {
                    'word': word,
                    'term_category': card['data']['category'],
                    'antonyms': antonyms}})
        cards.append(card)
    return HttpResponse(json.dumps(cards).encode('ascii', 'xmlcharrefreplace'),
            content_type='application/json')
