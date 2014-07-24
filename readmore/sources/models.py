from django.db import models
from polymorphic import PolymorphicModel
from readmore.sources.wikipedia import wiki_api

class Category(PolymorphicModel):
    parent = models.ForeignKey('self', null=True, blank=True,
        related_name='children')
    title = models.CharField(max_length=255)
    image = models.URLField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __repr__(self):
        return 'Category(%s)' % (self.title,)

    def __unicode__(self):
        return unicode(self.title)

    def get_subcategories(self, recursive=False):
        children = list(self.children.all())
        if recursive:
            for child in children:
                children += child.subcategories(recursive)
        return children

    def get_articles(self, recursive=False):
        articles = list(self.articles.all())
        if recursive:
            categories = self.get_subcategories(False)
            for category in categories:
                articles += category.get_articles(True)
        return articles

    def get_absolute_url(self):
        return "/sources/?category=%s" % (self.pk,)

class WikiCategory(Category):
    TYPES = (
        ('0', 'Page'),
        ('14','Category'),
        ('100', 'Portal')
    )
    identifier = models.CharField(max_length=255)
    wiki_type = models.CharField(max_length=3, choices=TYPES, default='14')

    class Meta:
        verbose_name_plural = "WikiCategories"

    def __repr__(self):
        return 'WikiCategory(%s)' % (self.identifier,)

    def __unicode__(self):
        return u'wikipedia::%s' % (self.title,)

    @staticmethod
    def factory(identifier):
        info = wiki_api.get_info(identifier)
        if info is not None:
            return WikiCategory(title=info['title'], wiki_type=info['ns'],
                identifier=identifier)
        else:
            return None

    def get_subcategories(self, recursive=False):
        # Retrieve any 'normal' subcategories
        subcategories = super(WikiCategory, self).get_subcategories(recursive)
        # Retrieve wikipedia subcategories if self is a category
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
        # Retrieve any 'normal' articles
        articles = super(WikiCategory, self).get_articles(False)
        # Retrieve wikipedia articles
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
        return "/sources/?category=%s&source=wikipedia" % (self.identifier,)


class Article(PolymorphicModel):
    category = models.ForeignKey('Category', related_name='articles')
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)

    def __repr__(self):
        return 'Article(%s)' % (self.title,)

    def __unicode__(self):
        return unicode(self.title)

    def get_body(self):
        return self.body

    def get_absolute_url(self):
        return "/sources/readmore/%d" % (self.pk,)

class WikiArticle(Article):
    identifier = models.CharField(max_length=255)

    def __repr__(self):
        return 'WikiArticle(%s)' % (self.identifier,)

    def __unicode__(self):
        return unicode(self.title)

    @staticmethod
    def factory(identifier):
        info = wiki_api.get_info(identifier)
        if info is not None:
            return WikiArticle(title=info['title'], identifier=identifier)
        else:
            return None

    def get_body(self):
        return wiki_api.get_page_text(self.identifier)

    def get_absolute_url(self):
        return "/sources/wikipedia/%s" % (self.identifier,)
