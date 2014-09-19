from django.shortcuts import render
from django.http import HttpResponse
from readmore.content.thirdparty.wiktionary_api import *
from cards import *
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
            cards.append(create_term_card(term))
            if isinstance(term, VerbTerm):
                cards.append(create_verb_conj_card(term))
        elif isinstance(term, TermForm):
            # Get main term
            main_term_info = api.get_info(term.main_term)
            if isinstance(term, VerbTermForm):
                main_terms = filter(
                    lambda x: isinstance(x, VerbTerm), main_term_info)
            elif isinstance(term, NounTermForm):
                main_terms = filter(
                    lambda x: isinstance(x, NounTerm), main_term_info)
            elif isinstance(term, AdjectiveTermForm):
                main_terms = filter(
                    lambda x: isinstance(x, AdjectiveTerm), main_term_info)
            else:
                main_terms = []
            if len(main_terms) == 1:
                cards.append(create_term_card(main_terms[0]))
                if isinstance(main_terms[0], VerbTerm):
                    cards.append(create_verb_conj_card(main_terms[0]))
    return HttpResponse(json.dumps(cards).encode('ascii', 'xmlcharrefreplace'),
            content_type='application/json')
