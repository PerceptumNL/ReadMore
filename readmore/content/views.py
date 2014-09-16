from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, \
        HttpResponseServerError
from django.conf import settings
import json
import requests
from readmore.content.models import *
import django.dispatch
from django.contrib.auth.decorators import login_required

article_read = django.dispatch.Signal(providing_args=["user", "category", "article_id", "article"])

def barrier(request):
    return render(request, 'barrier.html')

def update_feeds(request):
    for category in RSSCategory.objects.all():
        category.update_feed()
    return HttpResponse()

@login_required
def index(request):
    """Return response containing index of categories."""
    # Only show top categories on the index page
    categories = Category.objects.filter(parent=None)
    request.session['previous'] = ("", "")
    request.session['urls'] = [ ("Index","/") ]
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
    # Resolve identified category
    if source == "wikipedia":
        # Get/set identifier type
        identifier_type = request.GET.get('type','auto')
        category = WikiCategory.factory(identifier, identifier_type)
        if category is None:
            return render(request, 'unknowncategory.html')
    else:
        try:
            category = Category.objects.get(pk=int(identifier))
        except Category.DoesNotExist:
            return render(request, 'unknowncategory.html')
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
        # Update breadcrums
        urls = request.session.get('urls',[])
        if urls:
            request.session['previous'] = previous = urls[-1]
            current = [stripped(category.title), category.get_absolute_url()]
            if not current == previous:
                urls.append((stripped(category.title), category.get_absolute_url()))
                request.session['urls'] = urls
        else:
            urls.append(("Index","/"))
            urls.append((stripped(category.title), category.get_absolute_url()))
            request.session['previous'] = ("", "")
            request.session['urls'] = urls

        return render(request, 'navigation.html', {
            "crtCategory": category,
            "articles": articles,
            "subcategories": subcategories,
            "crumbs": request.session['urls']
    })

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
            return render(request, 'unknownarticle.html')
    else:
        try:
            # Attempt to retrieve the article
            article = Article.objects.get(pk=int(identifier))
        except Article.DoesNotExist:
            return render(request, 'unknownarticle.html')

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
                'body': article.get_body()
            }),
            content_type='application/json')

def about(request):
    return render(request, 'about.html')

