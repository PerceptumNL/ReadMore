from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, \
        HttpResponseServerError
from django.conf import settings
import json
import requests
from readmore.sources.models import *

def index(request):
    category = request.GET.get('category',None)
    source = request.GET.get('source', None)
    if category is None:
        # Show list of categories (remove `True or' later)
        categories = Category.objects.filter(parent=None)
        if True or request.is_ajax():
            # Return JSON list of categories with their properties
            categories = [{'url': c.get_absolute_url(), 'title': c.title,
                'image': c.image} for c in categories]
            return HttpResponse(json.dumps(categories),
                    content_type='application/json')
        else:
            # Return rendered HTML
            # return render("template", {'categories': categories})
            pass
    else:
        # Show list of articles and subcategories
        if source == "wikipedia":
            category_obj = WikiCategory.factory(category)
            if category_obj is None:
                return HttpResponseNotFound('Unknown category.')
        else:
            try:
                category_obj = Category.objects.get(pk=int(category))
            except Category.DoesNotExist:
                return HttpResponseNotFound('Unknown category.')

        articles = category_obj.get_articles()
        subcategories = category_obj.get_subcategories()
        if True or request.is_ajax():
            # Return JSON list of topics with their properties
            articles = [{'url': a.get_absolute_url(), 'title': a.title}
                for a in articles]
            subcategories = [{'url': c.get_absolute_url(), 'title': c.title, 'image': c.image}
                for c in subcategories]
            return HttpResponse(
                    json.dumps({
                        'articles': articles,
                        'subcategories': subcategories
                    }),
                    content_type='application/json')
        else:
            # Return rendered HTML
            # return render("template", {'articles': articles})
            pass


def article(request, identifier, source=None):
    if source == 'wikipedia':
        article = WikiArticle.factory(identifier)
        if article is None:
            return HttpResponseNotFound('Unknown article')
    else:
        try:
            article = Article.objects.get(pk=int(identifier))
        except Article.DoesNotExist:
            return HttpResponseNotFound('Unknown article')
    if True or request.is_ajax():
        # Return JSON with article properties
        return HttpResponse(
                json.dumps({
                    'title': article.title,
                    'body': article.get_body()
                }),
                content_type='application/json')
    else:
        # Return rendered HTML
        # return render("template", {'article': article})
        pass


def wiki_article(request, identifier):
    return article(request, identifier, source='wikipedia')
