from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, \
        HttpResponseServerError
from django.conf import settings
import json
import requests
from readmore.content.models import *

def index(request):
    """Return response containing index of categories."""
    # Only show top categories on the index page
    categories = Category.objects.filter(parent=None)
    # Render response
    if request.is_ajax():
        # Return JSON list of categories with their properties
        categories = [{'url': c.get_absolute_url(), 'title': c.title,
            'image': c.image} for c in categories]
        return HttpResponse(json.dumps(categories),
                content_type='application/json')
    else:
        # Render HTML of the landing page containing top categories
        counter = 0
        catList = []
        miniList = []
        for i in categories:
            counter +=1
            if counter < 3:
                miniList.append(i)
            else:
                miniList.append(i)
                counter = 0
                catList.append(miniList)
                miniList = []
        if(miniList != []):
            catList.append(miniList)
        return render(request, 'landing.html', { "categories": catList })

def category(request, identifier, source='local'):
    """Return response containing contents of identified category.

    The category is identified by a identifier and optionally a source. When
    the source is set to 'local', the identifier must be the primary key of a
    Category object. When the source is set to 'wikipedia', the identifier must
    correspond to either a pageid or a title of a wikipedia page.

    Named keywords:
    identifier -- Number or string identifying the category
    source -- The source the identifier belongs to ( default 'local' )
    """
    # Resolve identified category
    if source == "wikipedia":
        category = WikiCategory.factory(identifier)
        if category is None:
            return HttpResponseNotFound('Unknown category.')
    else:
        try:
            category = Category.objects.get(pk=int(identifier))
        except Category.DoesNotExist:
            return HttpResponseNotFound('Unknown category.')
    # Fetch any subcategories and articles contained in the category.
    articles = category.get_articles()
    subcategories = category.get_subcategories()
    # Render response

    if request.is_ajax():
        # Return JSON list of topics with their properties
        articles = [{'url': a.get_absolute_url(), 'title': a.title}
            for a in articles]
        subcategories = [{'url': c.get_absolute_url(), 'title': c.title,
            'image': c.image} for c in subcategories]
        return HttpResponse(
            json.dumps({
                'articles': articles,
                'subcategories': subcategories
            }),
            content_type='application/json')
    else:
        return render(request, 'navigation.html', {
            "crtCategory": category,
            "articles": articles,
            "subcategories": subcategories
    })

def article(request, identifier, source='local'):
    """Return response containing the identified article.

    The article is identified by a identifier and optionally a source. When
    the source is set to 'local', the identifier must be the primary key of a
    Category object. When the source is set to 'wikipedia', the identifier must
    correspond to either a pageid or a title of a wikipedia page.

    Named keywords:
    identifier -- Number or string identifying the category
    source -- The source the identifier belongs to ( default 'local' )
    """
    # Resolve identified article
    if source == 'wikipedia':
        # Get/set identifier type
        identifier_type = request.GET.get('type','auto')
        article = WikiArticle.factory(identifier, identifier_type)
        if article is None:
            return HttpResponseNotFound('Unknown article')
    else:
        try:
            article = Article.objects.get(pk=int(identifier))
        except Article.DoesNotExist:
            return HttpResponseNotFound('Unknown article')
    if request.is_ajax():
        # Return JSON with article properties
        return HttpResponse(
            json.dumps({
                'title': article.title,
                'body': article.get_body()
            }),
            content_type='application/json')
    else:
        return render(request, 'reader.html', { "article": article })
