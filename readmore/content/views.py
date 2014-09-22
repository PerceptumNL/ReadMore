from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, \
        HttpResponseServerError, HttpResponseRedirect
from django.conf import settings
import json
import requests
from readmore.content.models import *
import django.dispatch
from django.contrib.auth.decorators import login_required

article_read = django.dispatch.Signal(
        providing_args=["user", "category", "article_id", "article"])

def update_feeds(request):
    for category in RSSCategory.objects.all():
        category.update_feed()
    return HttpResponse()

@login_required
def index(request):
    """Return response containing overview of categories and articles."""
    # Only show top categories on the index page
    categories = Category.objects.filter(parent=None)
    articles = []
    for category in categories:
        articles += category.get_articles()
    # Render response
    if request.is_ajax():
        # Return JSON list of categories with their properties
        categories = [{'url': c.get_absolute_url(), 'title': c.title,
            'image': c.image} for c in categories]
        articles = [{'url': a.get_absolute_url(), 'title': a.title,
            'image': a.image} for a in articles]
        return HttpResponse(
                json.dumps({'categories': categories, 'articles': articles}),
                content_type='application/json')
    else:
        # Render HTML of the landing page containing top categories
        return render(request, 'overview.html',{
                "articles": articles,
                "categories": categories})

@login_required
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
    if not request.is_ajax():
        return HttpResponseRedirect('/')
    # Resolve identified category
    if source == "wikipedia":
        # Get/set identifier type
        identifier_type = request.GET.get('type','auto')
        category = WikiCategory.factory(identifier, identifier_type)
        if category is None:
            return HttpResponseRedirect('/')
    else:
        try:
            category = Category.objects.get(pk=int(identifier))
        except Category.DoesNotExist:
            return HttpResponseRedirect('/')
    # Fetch any subcategories and articles contained in the category.
    articles = []
    for article in category.get_articles():
        articles.append({
            'url': article.get_absolute_url(),
            'title': article.title,
            'category-color': category.color,
            'image': article.image if article.image else category.image})
    subcategories = [{'url': c.get_absolute_url(), 'title': c.title,
        'image': c.image} for c in category.get_subcategories()]
    # Return JSON list of topics with their properties
    return HttpResponse(json.dumps({'articles': articles,
            'subcategories': subcategories}), content_type='application/json')

@login_required
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
        # Attempt to retrieve the article
        article = WikiArticle.factory(identifier, identifier_type)
        if article is None:
            return HttpResponseRedirect('/')
    else:
        try:
            # Attempt to retrieve the article
            article = Article.objects.get(pk=int(identifier))
        except Article.DoesNotExist:
            return HttpResponseRedirect('/')

    # Retrieve the categories that this article belongs to.
    categories = article.get_categories()

    if not request.is_ajax():
        # Fetch random articles from the same categories for reading suggestions.
        random_articles = []
        for category in categories:
            random_articles += category.get_random_articles(2)

        # Ensure the current article is not suggested again
        if article in random_articles:
            random_articles.remove(article)

        # For all categories this article belongs to
        for category in categories:
            # If the category was stored in the database
            if category.pk is not None:
                article_read.send(
                        sender=Article,
                        user=request.user,
                        category=category,
                        article_id=identifier,
                        article=article)
        return render(request, 'articleView.html',
                {"article": article, "random_articles": random_articles})
    else:
        # Return JSON with article properties
        return HttpResponse(
            json.dumps({
                'title': article.title,
                'image': article.image,
                'body': article.get_body()
            }),
            content_type='application/json')
