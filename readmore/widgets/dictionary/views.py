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
    print "info: " + str(info)
    mainterm = []

    # For every Term and Form
    for types in info:
    	# If types is a Form, get the main term and append
    	if isinstance(types, TermForm):
    		term = api.get_info(types.main_term)
    		mainterm.append(term)
    		print "term: " + str(term)
    	# If types is a term, append
        else:
    	    mainterm.append(info)
    print "mainterm: " + str(mainterm)
    
    betekenis = [str(word) + " >> "]

    for termlist in mainterm:
    	for term in termlist:
    		print "term: " + str(term.entry)
    		betekenis.append(term.entry)
    		meaninglist = term.meanings
    		print "means: " + str(meaninglist)
    		betekenis.append('<ul>')
    		for meaning in meaninglist:
    			print "onemeaning: " + str(meaning)
    			betekenis.append('<li>' + str(meaning.definition) + '</li>')
    		betekenis.append('</ul>')

    return HttpResponse(json.dumps({'word':betekenis}),
            content_type='application/json')