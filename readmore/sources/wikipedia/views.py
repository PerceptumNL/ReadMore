from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from readmore.sources.wikipedia.wiki_api import *
import json

