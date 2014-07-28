from django.db import models
from polymorphic import PolymorphicModel
from readmore.sources.wikipedia import wiki_api

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

    # Link to a remotely hosted image.
    image = models.URLField(max_length=255, null=True, blank=True)

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

    def get_articles(self, recursive=False):
        """Return the list of articles in this catergory.
        Use this method to retrieve articles as it can be overriden by
        subclasses to give the expected result for each type of category.

        This function can search for all articles in all subcategories
        recursively, in a breadth-first search. This operation can however be
        rather costly.

        Keyword arguments:
        recursive -- Search for articles recursively (default False)
        """
        articles = list(self.articles.all())
        if recursive:
            categories = self.get_subcategories(False)
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
        return "/sources/?category=%s" % (self.pk,)

class WikiCategory(Category):
    """Model for wikipedia-based categories.

    A WikiCategory has besides a title and optionally an image, an identifier
    and a wiki_type. Each WikiCategory object may belong to a parent category.
    A parent category can contain multiple children categories.
    Apart from children, a category may also contain one or more articles.
    """

    # Possible values for wiki_type
    TYPES = (
        ('0', 'Page'),
        ('14','Category'),
        ('100', 'Portal')
    )

    # Identifier that corresponds to the identifier in the Wikipedia API
    identifier = models.CharField(max_length=255)

    # The type of this Wikipedia article.
    wiki_type = models.CharField(max_length=3, choices=TYPES, default='14')

    class Meta:
        verbose_name_plural = "WikiCategories"

    def __repr__(self):
        return 'WikiCategory(%s)' % (self.identifier,)

    def __unicode__(self):
        return u'wikipedia::%s' % (self.title,)

    @staticmethod
    def factory(identifier):
        """Return a WikiCategory instance based on the Wikipedia identifier.
        The title and type of the Wikipedia document refered to by the
        identifier is retrieved by *wiki_api.get_info*. The WikiCategory model
        instance returned is not saved to the database and will not have a
        primary key. If the identifier cannot be found on wikipedia,
        return None.
        """
        info = wiki_api.get_info(identifier)
        if info is not None:
            return WikiCategory(title=info['title'], wiki_type=str(info['ns']),
                identifier=identifier)
        else:
            return None

    def get_subcategories(self, recursive=False):
        """Return the list of subcategories.
        Use this method to retrieve subcategories as it can be overriden by
        subclasses to give the expected result for each type of category.

        This function can search for all subcategories recursively in a
        breadth-first search. This operation will almost certainly be costly.

        Subcategories can be retrieved from both explicit parent relationships
        in the database and from the Wikipedia API. The latter only applies
        when this WikiCategory has wiki_type 'Category'. The subcategories
        retrieved using *wiki_api.get_subcategories* are WikiCategory objects
        that are not saved in the database, and will not have a primary key.

        Keyword arguments:
        recursive -- Search for subcategories in all depths (default False)
        """
        # Retrieve any 'normal' subcategories
        subcategories = super(WikiCategory, self).get_subcategories(recursive)
        # Retrieve wikipedia subcategories if self is a wikipedia category
        if self.wiki_type == '14':
            subcats = wiki_api.get_subcategories(self.identifier, recursive)
            for cat in subcats:
                subcategories.append(WikiCategory(
                    parent=self,
                    title=cat['title'],
                    identifier=cat['pageid'],
                    wiki_type='14'))
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
        Wikipedia category retrieved using *wiki_api.get_page_links*. The
        articles retrieved from the Wikipedia API are WikiArticle objects that
        are not saved in the database, and as such will not have a primary key.

        Keyword arguments:
        recursive -- Search for subcategories in all depths (default False)
        """
        # Retrieve any 'normal' articles
        articles = super(WikiCategory, self).get_articles(False)
        # Retrieve Wikipedia articles
        links = wiki_api.get_page_links(self.identifier)
        for link in links:
            articles.append(WikiArticle(
                category=self,
                title=link['title'],
                identifier=link['pageid']))
        if recursive:
            # Retrieve articles from subcategories
            categories = self.get_subcategories(False)
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
        return "/sources/?category=%s&source=wikipedia" % (self.identifier,)


class Article(PolymorphicModel):
    """Basic DB model for articles.

    Extends the PolymorphicModel class to dynamically handle inheritence.
    An article has a title and optionally a body. Each Article object
    belongs to a category.
    """
    category = models.ForeignKey('Category', related_name='articles')
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)

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

    def get_absolute_url(self):
        """Return the URL identifiying this object.
        Use this method to form an identification URL as it can be overriden by
        subclasses to contain the right information for each type of category.
        See also:
        https://docs.djangoproject.com/en/1.6/ref/models/instances/#django.db.models.Model.get_absolute_url
        """
        return "/sources/readmore/%d" % (self.pk,)

class WikiArticle(Article):
    """Model for wikipedia-based articles.

    A WikiArticle has a title and a wikipedia identifier.
    Each WikiArticle object belongs to a category.
    """

    # Identifier that corresponds to the identifier in the Wikipedia API
    identifier = models.CharField(max_length=255)

    def __repr__(self):
        return 'WikiArticle(%s)' % (self.identifier,)

    def __unicode__(self):
        return unicode(self.title)

    @staticmethod
    def factory(identifier):
        """Return a WikiArticle instance based on the Wikipedia identifier.
        The title of the Wikipedia article refered to by the identifier is
        retrieved by *wiki_api.get_info*. The WikiArticle model instance
        returned is not saved to the database and will not have a primary key.
        If the identifier cannot be found on wikipedia, return None.
        """
        info = wiki_api.get_info(identifier)
        if info is not None:
            return WikiArticle(title=info['title'], identifier=identifier)
        else:
            return None

    def get_body(self):
        """Return the body of this article.
        Use this method to retrieve the body as it can be overriden by
        subclasses to give the expected result for each type of article.

        The body text is retrieved using *wiki_api.get_page_text*.
        """
        return wiki_api.get_page_text(self.identifier)

    def get_absolute_url(self):
        """Return the URL identifiying this object.
        Use this method to form an identification URL as it can be overriden by
        subclasses to contain the right information for each type of category.
        See also:
        https://docs.djangoproject.com/en/1.6/ref/models/instances/#django.db.models.Model.get_absolute_url
        """
        return "/sources/wikipedia/%s" % (self.identifier,)
