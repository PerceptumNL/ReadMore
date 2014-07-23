from django.db import models

# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=255)
    icon = models.URLField(max_length=255)

    def __repr__(self):
        return 'Topic(%s)' % (self.title,)

    def __unicode__(self):
        return unicode(self.title)

class Category(models.Model):
    topic = models.ForeignKey('Topic')
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __repr__(self):
        return 'Category(%s)' % (self.title,)

    def __unicode__(self):
        return unicode(self.title)

class Article(models.Model):
    topic = models.ForeignKey('Topic')
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __repr__(self):
        return 'Article(%s)' % (self.title,)

    def __unicode__(self):
        return unicode(self.title)

class ExternalArticle(models.Model):
    topic = models.ForeignKey('Topic')
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)

    def __repr__(self):
        return 'ExternalArticle(%s::%s)' % (self.source, self.title,)

    def __unicode__(self):
        return u'%s::%s' % (self.source, self.title)
