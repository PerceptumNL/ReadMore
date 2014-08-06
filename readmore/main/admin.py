from django.contrib import admin
from models import *

# Register your models here.
class CounterBadgeInline(admin.StackedInline):
    model = CounterBadge
    extra = 0
    
class BadgeAdmin(admin.ModelAdmin):
    base_model = Badge
    inlines = [
        CounterBadgeInline,
    ]
    
class StatisticsAdmin(admin.ModelAdmin):
    base_model = Statistics
    list_display = ('user', 'docsRead')
    
admin.site.register(Badge, BadgeAdmin)    
admin.site.register(Statistics, StatisticsAdmin)
