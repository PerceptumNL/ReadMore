from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from polymorphic import PolymorphicModel
from readmore.content.thirdparty.wiki_api import MediaWikiAPI, NS_PAGE, \
        NS_CATEGORY, NS_PORTAL
from readmore.content.helpers import *
import lxml
import random
import urllib
import re
from datetime import datetime
from time import mktime
import feedparser
from bs4 import BeautifulSoup

MWAPI = MediaWikiAPI()

class Category(PolymorphicModel):
    """Basic DB model for categories.

    Extends the PolymorphicModel class to dynamically handle inheritence.
    A category has a title and optionally an image. Each Category object may
    belong to a parent category. A parent category can contain multiple
    children categories. Apart from children, a category may also contain
    one or more articles.
    """

    parent = models.ForeignKey('self', null=True, blank=True,
        related_name='children')
    title = models.CharField(max_length=255)
    color = models.CharField(max_length=50, default='#f3f3f3', blank=True)

    # Link to a remotely hosted image.
    image = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __repr__(self):
        return 'Category(%s)' % (self.title,)

    def __unicode__(self):
        return unicode(self.title)

    def get_subcategories(self, recursive=False):
        """Return the list of subcategories.
        Use this method to retrieve subcategories as it can be overriden by
        subclasses to give the expected result for each type of category.

        This function can search for all subcategories recursively in a
        breadth-first search. This operation can however be rather costly.

        Keyword arguments:
        recursive -- Search for subcategories in all depths (default False)
        """
        children = list(self.children.all())
        if recursive:
            for child in children:
                children += child.subcategories(recursive)
        return children

    def get_articles(self, recursive=False, max_num='Inf'):
        """Return the list of articles in this catergory.
        Use this method to retrieve articles as it can be overriden by
        subclasses to give the expected result for each type of category.

        This function can search for all articles in all subcategories
        recursively, in a breadth-first search. This operation can however be
        rather costly.

        Keyword arguments:
        recursive -- Search for articles recursively (default False)
        max_num -- Maximum number of articles (default 'Inf')
        """
        articles = list(self.articles.all())
        if recursive and len(articles) < max_num:
            categories = self.get_subcategories(False)
            for category in categories:
                if len(articles) < max_num:
                    articles += category.get_articles(True, max_num)
        if max_num == 'Inf':
            return articles
        else:
            return articles[:max_num]

    def get_random_articles(self, num=5, read_by_user=None):
        """Return a number of random articles.

        Keyword arguments:
        num -- The number of random articles to return (default 5)
        """
        article_list = self.get_articles()
        if read_by_user is not None:
            article_list = [article for article in article_list if article.pk not in read_by_user]
        random.shuffle(article_list)
        return article_list[:num]

    def get_absolute_url(self):
        """Return the URL identifiying this object.
        Use this method to form an identification URL as it can be overriden by
        subclasses to contain the right information for each type of category.
        See also:
        https://docs.djangoproject.com/en/1.6/ref/models/instances/#django.db.models.Model.get_absolute_url
        """
        return reverse('category', args=(self.pk,))


class RSSCategory(Category):
    """Model for RSS-based categories."""
    feed = models.URLField()
    last_update = models.DateTimeField(null=True, blank=True)

    def get_articles(self, recursive=False, max_num=100):
        """Return the list of articles in this catergory.
        Use this method to retrieve articles as it can be overriden by
        subclasses to give the expected result for each type of category.

        This function can search for all articles in all subcategories
        recursively, in a breadth-first search. This operation can however be
        rather costly.

        Keyword arguments:
        recursive -- Search for articles recursively (default False)
        max_num -- Maximum number of articles (default 100)
        """
        articles = super(RSSCategory, self).get_articles(recursive, 'Inf')
        articles = sorted(articles, key=lambda a: a.publication_date,
                reverse=True)
        if max_num == 'Inf':
            return articles
        else:
            return articles[:max_num]

    def update_feed(self):
        """Retrieve new articles from the RSS feed in this category."""
        re_image = re.compile("^image/")
        data = feedparser.parse(self.feed)
        if 'updated_parsed' in data:
            updated = datetime.fromtimestamp(mktime(data['updated_parsed']))
        elif 'published_parsed' in data:
            updated = datetime.fromtimestamp(mktime(data['published_parsed']))
        else:
            updated = datetime.now()
        if timezone.is_naive(updated):
            updated = timezone.make_aware(updated, timezone.utc)
        last_updated = self.last_update if self.last_update else \
                datetime.fromtimestamp(0)
        if timezone.is_naive(last_updated):
            last_updated = timezone.make_aware(last_updated, timezone.utc)
        if updated > last_updated:
            for entry in data['entries']:
                published = datetime.fromtimestamp(
                        mktime(entry['published_parsed']))
                if timezone.is_naive(published):
                    published = timezone.make_aware(published, timezone.utc)
                if published > last_updated:
                    if 'content' in entry:
                        body = entry['content'][0]['value']
                    elif 'description' in entry:
                        body = entry['description']
                    elif 'summary' in entry:
                        body = entry['summary']
                    else:
                        continue
                    parse_body = BeautifulSoup(body)
                    # Remove existing images in the body
                    for image in parse_body.find_all('img'):
                        image.decompose()
                    # Remove existing links in the body
                    for link in parse_body.find_all('a'):
                        if link.string:
                            link.replace_with(link.string)
                        else:
                            link.decompose()
                    body = str(parse_body)
                    if 'links' in entry:
                        images = filter(lambda x: re_image.match(x['type']),
                                entry['links'])
                        main_image = images.pop(0)['href'] if images else None
                        for image in images:
                            body += '<img src="%s" />' % (image['href'],)
                    else:
                        main_images = None
                        images = []
                    article, created = RSSArticle.objects.get_or_create(
                            identifier=entry['id'],
                            defaults={
                                'title': entry['title'],
                                'body': body,
                                'image': main_image,
                                'publication_date': published
                            })
                    article.categories.add(self)
                    article.save()
            self.last_update = updated
            super(RSSCategory, self).save()

    def save(self, *args, **kwargs):
        super(RSSCategory, self).save(*args, **kwargs)
        self.update_feed()


class WikiCategory(Category):
    """Model for wikipedia-based categories.

    A WikiCategory has besides a title and optionally an image, an identifier
    and a wiki_type. Each WikiCategory object may belong to a parent category.
    A parent category can contain multiple children categories.
    Apart from children, a category may also contain one or more articles.
    """

    # Possible values for wiki_type
    TYPES = (
        (NS_PAGE, 'Page'),
        (NS_CATEGORY,'Category'),
        (NS_PORTAL, 'Portal')
    )

    ID_TYPES = (
        ('pageid', 'pageid'),
        ('title', 'title')
    )

    # Identifier that corresponds to the identifier in the Wikipedia API
    identifier = models.CharField(max_length=255)

    # The type of identifier
    identifier_type = models.CharField(max_length=6, choices=ID_TYPES,
            default='title', blank=True)

    # The type of this Wikipedia article.
    wiki_type = models.CharField(max_length=3, choices=TYPES,
            default=NS_CATEGORY)

    class Meta:
        verbose_name_plural = "WikiCategories"

    def __repr__(self):
        return 'WikiCategory(%s)' % (self.identifier,)

    def __unicode__(self):
        return u'wikipedia::%s' % (self.title,)

    @staticmethod
    def factory(identifier, identifier_type='auto'):
        """Return a WikiCategory instance based on the Wikipedia identifier.
        The title and type of the Wikipedia document refered to by the
        identifier is retrieved by *MediaWikiAPI.get_info*. The WikiCategory model
        instance returned is not saved to the database and will not have a
        primary key. If the identifier cannot be found on wikipedia,
        return None.

        Keyword arguments:
        identifier -- Identifier of the wikipedia article
        identifier_type -- Type of identifier [pageid, title, auto]
        """
        if identifier_type == "auto" and identifier.isdigit():
            identifier_type = "pageid"
        elif identifier_type == "auto":
            identifier_type = "title"
        elif identifier_type not in dict(WikiCategory.ID_TYPES):
            raise ValueError("%s is not a valid identifier type" %
                    (identifier_type,))

        if identifier_type == "pageid":
            info = MWAPI.get_info(int(identifier))
        else:
            info = MWAPI.get_info(identifier)

        if info is not None:
            return WikiCategory(title=info['title'], wiki_type=str(info['ns']),
                identifier=identifier)
        else:
            return None

    def get_identifier(self):
        """Return a casted identifier, based on the identifier_type."""
        types = dict(self.ID_TYPES)
        if self.identifier_type == types['pageid']:
            return int(self.identifier)
        else:
            return self.identifier

    def get_subcategories(self, recursive=False):
        """Return the list of subcategories.
        Use this method to retrieve subcategories as it can be overriden by
        subclasses to give the expected result for each type of category.

        This function can search for all subcategories recursively in a
        breadth-first search. This operation will almost certainly be costly.

        Subcategories can be retrieved from both explicit parent relationships
        in the database and from the Wikipedia API. The latter only applies
        when this WikiCategory has wiki_type 'Category'. The subcategories
        retrieved using *MediaWikiAPI.get_subcategories* are WikiCategory objects
        that are not saved in the database, and will not have a primary key.

        Keyword arguments:
        recursive -- Search for subcategories in all depths (default False)
        """
        # Retrieve any 'normal' subcategories
        subcategories = super(WikiCategory, self).get_subcategories(recursive)
        # Retrieve wikipedia subcategories if self is a wikipedia category
        if self.wiki_type == NS_CATEGORY:
            subcats = MWAPI.get_category_members(
                    self.get_identifier(), recursive=recursive)
            for cat in subcats:
                subcategories.append(WikiCategory(
                    parent=self,
                    title=stripped(cat['title']),
                    identifier=cat['pageid'],
                    identifier_type='pageid',
                    wiki_type=NS_CATEGORY))
        return subcategories

    def get_articles(self, recursive=False):
        """Return the list of articles in this catergory.
        Use this method to retrieve articles as it can be overriden by
        subclasses to give the expected result for each type of category.

        This function can search for all articles in all subcategories
        recursively, in a breadth-first search. This operation will almost
        certainly be costly.

        Subcategories can be retrieved from both explicit Article.category
        relationships in the database and from the links in the body of this
        Wikipedia category retrieved using *MediaWikiAPI.get_page_links*. The
        articles retrieved from the Wikipedia API are WikiArticle objects that
        are not saved in the database, and as such will not have a primary key.

        Keyword arguments:
        recursive -- Search for subcategories in all depths (default False)
        """
        # Retrieve any 'normal' articles
        articles = super(WikiCategory, self).get_articles(False)
        # Retrieve Wikipedia articles
        if self.wiki_type == NS_CATEGORY:
            members = MWAPI.get_category_members(self.get_identifier(),
                    namespace=NS_PAGE)
        else:
            members = MWAPI.get_page_links(self.get_identifier())

        for member in members:
            articles.append(WikiArticle(
                category=self,
                title=member['title'],
                identifier=member['pageid'],
                identifier_type='pageid')),
        if recursive:
            # Retrieve articles from subcategories
            categories = self.get_category_members(recursive=False)
            for category in categories:
                articles += category.get_articles(True)
        return articles

    def get_absolute_url(self):
        """Return the URL identifiying this object.
        Use this method to form an identification URL as it can be overriden by
        subclasses to contain the right information for each type of category.
        See also:
        https://docs.djangoproject.com/en/1.6/ref/models/instances/#django.db.models.Model.get_absolute_url
        """
        return "%s?type=%s" % (
                reverse('wikipedia_category', args=(self.identifier,)),
                self.identifier_type)


class Article(PolymorphicModel):
    """Basic DB model for articles.

    Extends the PolymorphicModel class to dynamically handle inheritence.
    An article has a title and optionally a body. Each Article object
    belongs to a category.
    """
    categories = models.ManyToManyField('Category', related_name='articles')
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)

    def __repr__(self):
        return 'Article(%s)' % (self.title,)

    def __unicode__(self):
        return unicode(self.title)

    def get_body(self):
        """Return the body of this article.
        Use this method to retrieve the body as it can be overriden by
        subclasses to give the expected result for each type of article.
        """
        return self.body

    def get_extract(self, chars=500):
        """Return an extract of given size from this article.
        Use this method to retrieve the body as it can be overriden by
        subclasses to give the expected result for each type of article.

        Keywords arguments:
        chars -- Length of extract in number of characters (default 100)
        """
        return self.body[:chars-3]+"..."

    def get_categories(self):
        """Return the categories this articles is in.
        Use this method to retrieve the categories as it can be overriden by
        subclasses to contain the right information for each type of article.
        """
        return self.categories.all()

    def get_absolute_url(self):
        """Return the URL identifiying this object.
        Use this method to form an identification URL as it can be overriden by
        subclasses to contain the right information for each type of category.
        See also:
        https://docs.djangoproject.com/en/1.6/ref/models/instances/#django.db.models.Model.get_absolute_url
        """
        return reverse('article', args=(self.pk,))


class RSSArticle(Article):
    """Model for RSS-based articles."""
    publication_date = models.DateTimeField()
    identifier = models.URLField(max_length=255)


class WikiArticle(Article):
    """Model for wikipedia-based articles.

    A WikiArticle has a title and a wikipedia identifier.
    Each WikiArticle object belongs to a category.
    """
    ID_TYPES = (
        ('pageid', 'pageid'),
        ('title', 'title')
    )

    # Identifier that corresponds to the identifier in the Wikipedia API
    identifier = models.CharField(max_length=255)
    identifier_type = models.CharField(max_length=6, choices=ID_TYPES,
            default='title', blank=True)

    def __repr__(self):
        return 'WikiArticle(%s)' % (self.identifier,)

    def __unicode__(self):
        return unicode(self.title)

    @staticmethod
    def factory(identifier, identifier_type="auto"):
        """Return a WikiArticle instance based on the Wikipedia identifier.
        The title of the Wikipedia article refered to by the identifier is
        retrieved by *MediaWikiAPI.get_info*. The WikiArticle model instance
        returned is not saved to the database and will not have a primary key.
        If the identifier cannot be found on wikipedia, return None.

        Keyword arguments:
        identifier -- Identifier of the wikipedia article
        identifier_type -- Type of identifier [pageid, title, auto]
        """
        if identifier_type == "auto" and identifier.isdigit():
            identifier_type = "pageid"
        elif identifier_type == "auto":
            identifier_type = "title"
        elif identifier_type not in dict(WikiArticle.ID_TYPES):
            raise ValueError("%s is not a valid identifier type" %
                    (identifier_type,))

        if identifier_type == "pageid":
            info = MWAPI.get_info(int(identifier))
        else:
            info = MWAPI.get_info(identifier)

        if info is not None:
            return WikiArticle(title=info['title'], identifier=identifier,
                    identifier_type=identifier_type)
        else:
            return None

    def get_identifier(self):
        """Return a casted identifier, based on the identifier_type."""
        types = dict(self.ID_TYPES)
        if self.identifier_type == types['pageid']:
            return int(self.identifier)
        else:
            return self.identifier

    def get_body(self):
        """Return the body of this article.
        Use this method to retrieve the body as it can be overriden by
        subclasses to give the expected result for each type of article.

        The body text is retrieved using *MediaWikiAPI.get_page_text*.
        """
        return process_wiki_page_html(
                MWAPI.get_page_text(self.get_identifier()))

    def get_extract(self, chars=500):
        """Return an extract of given size from this article.
        Use this method to retrieve the body as it can be overriden by
        subclasses to give the expected result for each type of article.

        The body text is retrieved using *MediaWikiAPI.get_page_extract*.

        Keywords arguments:
        chars -- Length of extract in number of characters (default 100)
        """
        return MWAPI.get_page_extract(self.get_identifier(), chars=chars)

    def get_categories(self):
        """Return the categories this articles is in.
        Use this method to retrieve the categories as it can be overriden by
        subclasses to contain the right information for each type of article.
        """
        return MWAPI.get_page_categories(self.get_identifier())

    def get_absolute_url(self):
        """Return the URL identifiying this object.
        Use this method to form an identification URL as it can be overriden by
        subclasses to contain the right information for each type of category.
        See also:
        https://docs.djangoproject.com/en/1.6/ref/models/instances/#django.db.models.Model.get_absolute_url
        """
        return "%s?type=%s" % (
                reverse('wikipedia_article', args=(self.identifier,)),
                self.identifier_type)

