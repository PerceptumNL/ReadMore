from django.db import models
from django.contrib.auth.models import User

class CustomCard(models.Model):
    word = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User)

    def __str__(self):
        return "Message about \"%s\" from %s" % (
                self.word.encode('utf8'), self.user)
