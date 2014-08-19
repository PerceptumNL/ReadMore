from django.db import models
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from readmore.content.views import article_read
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)       
    badges = models.ManyToManyField('Badge')
    school = models.CharField(max_length=255)
    
    
class Statistics(models.Model):
    STATS = [('docsRead','docsRead')]

    user = models.ForeignKey(User, unique=True)
    docsRead = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "User Statistics"

    def __repr__(self):
        return 'Statistics (%s)' % (self.user.username,)

    def __unicode__(self):
        name = 'Statistics (%s)' % (self.user.username,)
        return unicode(name)
        
class History(models.Model):
    user = models.ForeignKey(User, unique=True)
    opened = models.DateTimeField(auto_now_add=True)        
    article_id = models.CharField(max_length=255)
        
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
        #print "Article Read Signal received for %s with id=%s" % (user, article.title)
        #print "Total articles read by %s  is now (%s)" % (user, str(statistics_of_user.docsRead))
    except:
        #print "No statistics in database for (%s)" % (user)
        pass
    try:
        article_in_current_history = History.objects.filter(user=user, article_id=article_id)
        if not article_in_current_history:
            new_history_of_user = History.objects.create(user=user, article_id=article_id)
            new_history_of_user.save()
    except:
        pass
        
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

class CounterBadge(models.Model):
    badge = models.ForeignKey(Badge)
    trigger_at_greater_than = models.IntegerField(default=0)
    image = models.URLField(max_length=255, null=True, blank=True)
    
    class Meta:
        ordering = ('trigger_at_greater_than',)
        


