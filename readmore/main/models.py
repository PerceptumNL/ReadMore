from __future__ import absolute_import

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import timezone
from django.utils import formats
from django.core.urlresolvers import reverse
from django.core.signals import request_started
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

import pytz
from polymorphic import PolymorphicModel
import allauth.app_settings
from allauth.socialaccount import providers

from collections import Counter
import operator

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    badges = models.ManyToManyField('Badge', blank=True, related_name='users')
    groups = models.ManyToManyField('Group', blank=True, related_name='users')
    #study_groups = models.ManyToManyField('Group', blank=True, related_name='users')
    institute = models.ForeignKey('Institute', blank=True, null=True,
            related_name='users')

    def __unicode__(self):
        return unicode(self.user)

    def __str__(self):
        return unicode(self).encode('utf-8')


class Institute(models.Model):
    title = models.CharField(max_length=255)
    site_id = models.ForeignKey(Site)
    timezone = models.CharField(max_length=100,
            choices=zip(pytz.common_timezones, pytz.common_timezones))
    provider = models.CharField(verbose_name=('provider'),
                                max_length=30,
                                choices=providers.registry.as_choices())

    @staticmethod
    @receiver(request_started)
    def set_current_timezone(*args, **kwargs):
        try:
            institute = Institute.objects.get(
                    site_id=Site.objects.get_current())
        except Institute.DoesNotExist:
            pass
        else:
            timezone.activate(institute.timezone)

    def __repr__(self):
        return '%s' % (self.title)

    def __unicode__(self):
        return unicode(self.title)


class Group(models.Model):
    title = models.CharField(max_length=255)
    leader = models.ForeignKey(User, null=True, blank=True)
    institute = models.ForeignKey('Institute', null=True, blank=True)

    def __unicode__(self):
        return u'Group of %s' % (self.leader,)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def get_popular_articles(self, number, user_profile, read_articles):
        """Return a number of popular articles in this group.

        Keyword Arguments:
            number -- the number of articles to be returned
            user_profile -- the user to be excluded from 
            the user set

        Returns:
            popular_articles -- a list of length number 
            containing the most popular articles in 
            this group
        """
        # Get all other users in this group
        users = list(self.users.all())
        # Remove current user from list
        users.remove(user_profile[0])
        #Get article events belonging to these users, sorted by most recent
        article_histories = ArticleHistoryItem.objects.filter(user__in=users).order_by('-id')[:100]

        #Get list of article objects
        article_list = [a_h.article for a_h in article_histories]
        
        for article in article_list:
            if article.pk in read_articles:
                article_list.remove(article)

        #Count article appearances for later sorting
        article_counts = dict(Counter(article_list))

        count = 0
        popular_articles = []
        #Get most read articles
        for art in sorted(article_counts.items(), key=operator.itemgetter(1), reverse=True):
            #If this article has an image, save it
            if art[0].image:
                popular_articles.append(art[0])
                count += 1
            if count == number:
                break
        return popular_articles


class Event(PolymorphicModel):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return u'Event'

    def __str__(self):
        return unicode(self).encode('utf-8')

    def describe(self):
        """Return a dictionary-like object with key properties."""
        displayname = (lambda user: u' '.join([user.first_name, user.last_name])
                if user.first_name else user.username)
        return {'type': 'event',
                'date': formats.date_format(
                    timezone.localtime(self.date),
                    "DATETIME_FORMAT"),
                'user': unicode(displayname(self.user))
                }


class ArticleHistoryItem(Event):
    article = models.ForeignKey('content.Article')

    def __unicode__(self):
        return u'%s' % (self.article.title,)

    def describe(self):
        """Return a dictionary-like object with key properties."""
        desc = super(ArticleHistoryItem, self).describe()
        desc = {} if desc is None else desc
        desc.update({
            'type': 'event-article-view',
            'article': {
                'url': reverse('article', args=(self.article.id,)),
                'title': unicode(self.article)
                }
            })
        return desc


class ArticleRatingItem(Event):
    article = models.ForeignKey('content.Article')
    rating = models.IntegerField()

    def __unicode__(self):
        return u'%s' % (self.article.title,)

    def describe(self):
        """Return a dictionary-like object with key properties."""
        desc = super(ArticleRatingItem, self).describe()
        desc = {} if desc is None else desc
        desc.update({
            'type': 'event-article-rating',
            'rating': str(self.rating),
            'article': {
                'url': reverse('article', args=(self.article.id,)),
                'title': unicode(self.article)
                }
            })
        return desc


class ArticleDifficultyItem(Event):
    article = models.ForeignKey('content.Article')
    rating = models.IntegerField()

    def __unicode__(self):
        return u'%s' % (self.article.title,)

    def describe(self):
        """Return a dictionary-like object with key properties."""
        desc = super(ArticleDifficultyItem, self).describe()
        desc = {} if desc is None else desc
        desc.update({
            'type': 'event-article-difficulty',
            'rating': str(self.rating),
            'article': {
                'url': reverse('article', args=(self.article.id,)),
                'title': unicode(self.article)
                }
            })
        return desc


class WordHistoryItem(Event):
    article = models.ForeignKey('content.Article')
    word = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % (self.word,)

    def describe(self):
        """Return a dictionary-like object with key properties."""
        desc = super(WordHistoryItem, self).describe()
        desc = {} if desc is None else desc
        desc.update({
            'type': 'event-word-cover',
            'word': unicode(self.word),
            'article': {
                'url': reverse('article', args=(self.article.id,)),
                'title': unicode(self.article)
                }
            })
        return desc


class Statistics(models.Model):
    STATS = [('docsRead','docsRead')]

    user = models.ForeignKey(User, unique=True, related_name='statistics')
    docsRead = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "User Statistics"

    def __repr__(self):
        return 'Statistics (%s)' % (self.user.username,)

    def __unicode__(self):
        name = 'Statistics (%s)' % (self.user.username,)
        return unicode(name)

class History(models.Model):
    user = models.ForeignKey(User)
    opened = models.DateTimeField(auto_now_add=True)
    article_id = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = "Article History"

    def __repr__(self):
        return self.article_id

    def __unicode__(self):
        return unicode(self.article_id)   
        
    
@receiver(user_signed_up)
def connect_statistics_to_user(sender, request, user, **kw):
    statistics = Statistics(user=user)
    statistics.save()
    #print "Created Statistics for %s" % (user)


# Create your models here.
class Badge(models.Model):
    title = models.CharField(max_length=255)
    default_image = models.URLField(max_length=255, null=True, blank=True)
    field_to_listen_to = models.CharField(max_length=255, choices = Statistics.STATS)
    
    class Meta:
        verbose_name_plural = "Badges"

    def __repr__(self):
        return 'Badge (%s)' % (self.title,)

    def __unicode__(self):
        return unicode(self.title)

    def current_image(self, user):
        badge_image = self.default_image
        statistics = Statistics.objects.get(user=user)
        statistic = getattr(statistics, self.field_to_listen_to)
        counter_badges = CounterBadge.objects.filter(badge=self)
        for counter_badge in counter_badges.reverse():
            if counter_badge.trigger_at_greater_than <= statistic:
                badge_image = counter_badge.image
                break
        return badge_image
        

class CounterBadge(models.Model):
    badge = models.ForeignKey(Badge, related_name='counter_badges')
    trigger_at_greater_than = models.IntegerField(default=0)
    image = models.URLField(max_length=255, null=True, blank=True)
    
    class Meta:
        ordering = ('trigger_at_greater_than',)
        


