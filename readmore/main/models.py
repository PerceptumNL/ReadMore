from __future__ import absolute_import

from django.db import models
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from readmore.content.views import article_read
from django.dispatch import receiver

import allauth.app_settings
from allauth.socialaccount import providers

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)       
    badges = models.ManyToManyField('Badge', blank='True')
    school = models.CharField(max_length=255)

class Institute(models.Model):
    title = models.CharField(max_length=255)
    provider = models.CharField(verbose_name=('provider'),
                                max_length=30,
                                choices = providers.registry.as_choices())
    def __repr__(self):
        return '%s' % (self.title)

    def __unicode__(self):
        return unicode(self.title)

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
        statistics_of_user = Statistics.objects.get(user=user)
        statistics_of_user.docsRead += 1
        statistics_of_user.save()
    except:
        #print "No statistics in database for (%s)" % (user)
        pass
        
    # Check for new badges
    all_badges = Badge.objects.all()
    statistics = Statistics.objects.get(user=user)
    for badge in all_badges:
        counter_badges = CounterBadge.objects.filter(badge=badge)
        if len(counter_badges)>0:
            statistic = getattr(statistics, badge.field_to_listen_to)
            if(statistic>=counter_badges[0].trigger_at_greater_than):
                user.userprofile.badges.add(badge)       
        
    try:
        article_in_current_history = History.objects.get(user=user, article_id=article_id)       
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
        


