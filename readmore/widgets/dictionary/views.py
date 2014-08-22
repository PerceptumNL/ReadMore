from django.shortcuts import render
from django.http import HttpResponse
from readmore.content.thirdparty.wiktionary_api import *
import json

# Create your views here.
def process(request):
    word = request.GET.get('word',"No word given")
    
    api = WiktionaryAPI(languages=['nld'])

    # Get list of Terms and Forms for word
    try: 
        info = api.get_info(word)
    except Exception:
        info = []
    
    mainterm = []

    # For every Term and Form
    if(info != []):
        for types in info:
        	# If types is a Form, get the main term and append
            if isinstance(types, TermForm):
                # TODO: Use types.form2text() to get human-readable text
                term = api.get_info(types.main_term)
                mainterm.append(term)
        	# If types is a term, append
            else:
                mainterm.append(info)

        for termlist in mainterm:
            for term in termlist:
                if(isinstance(term, TermForm)):
                    pass
                else:
                    betekenis = ["<h3 class='title'>" + str(word) + " >> " + str(term.entry) + "</h3>"]
                    meaninglist = term.meanings
                    betekenis.append('<ul>')
                    for meaning in meaninglist:
                        betekenis.append('<li>%s</li>' % (
                            meaning.definition.encode('ascii',
                                'xmlcharrefreplace')))
                    betekenis.append('</ul>')

    else:
        betekenis = "<h3 class='title'>Woordenboek</h3><p><span class='notfound'>" + str(word) + "</span> is niet gevonden!</p>"
    return HttpResponse(json.dumps({'word':betekenis}),
            content_type='application/json')
