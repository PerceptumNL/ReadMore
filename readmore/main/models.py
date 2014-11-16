from __future__ import absolute_import

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.signals import request_started
from allauth.account.signals import user_signed_up
from readmore.content.views import article_read
from django.dispatch import receiver

import pytz
from polymorphic import PolymorphicModel
import allauth.app_settings
from allauth.socialaccount import providers

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    badges = models.ManyToManyField('Badge', blank=True, related_name='users')
    groups = models.ManyToManyField('Group', blank=True, related_name='users')
    institute = models.ForeignKey('Institute', blank=True, null=True,
            related_name='users')


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
        return {'type': 'event',
                'date': str(timezone.localtime(self.date)),
                'user': unicode(self.user).encode(
                    'ascii', 'xmlcharrefreplace')
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
                'title': unicode(self.article).encode(
                    'ascii', 'xmlcharrefreplace')
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
                'title': unicode(self.article).encode(
                    'ascii', 'xmlcharrefreplace')
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
                'title': unicode(self.article).encode(
                    'ascii', 'xmlcharrefreplace')
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
            'word': unicode(self.word).encode(
                'ascii', 'xmlcharrefreplace'),
            'article': {
                'url': reverse('article', args=(self.article.id,)),
                'title': unicode(self.article).encode(
                    'ascii', 'xmlcharrefreplace')
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

@receiver(article_read)
def add_to_statistics(sender, user, category, article_id, article, **kw):
    try:
        statistics = Statistics.objects.get(user=user)
        statistics.docsRead += 1
        statistics.save()
        # Check for new badges
        all_badges = Badge.objects.all()
        for badge in all_badges:
            counter_badges = CounterBadge.objects.filter(badge=badge)
            if len(counter_badges)>0:
                statistic = getattr(statistics, badge.field_to_listen_to)
                if(statistic>=counter_badges[0].trigger_at_greater_than):
                    user.userprofile.badges.add(badge)
    except:
        #print "No statistics in database for (%s)" % (user)
        pass
    try:
        article_in_current_history = History.objects.get(user=user,
                article_id=article_id)
    except History.DoesNotExist:
        new_history_of_user = History.objects.create(user = user)
        new_history_of_user.article_id = article_id
        new_history_of_user.save()
        
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
        


