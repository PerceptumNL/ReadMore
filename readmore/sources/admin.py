from django.contrib import admin
from readmore.sources.models import *

admin.site.register(Topic)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(ExternalArticle)

