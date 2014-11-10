from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from models import *

class InstituteAdmin(admin.ModelAdmin):
    base_model = Institute
    list_display = ('title', 'provider')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    filter_horizontal = ('badges',)

class CustomUserAdmin(UserAdmin):
    save_on_top = True
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')
    inlines = [UserProfileInline]


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
    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Institute, InstituteAdmin)
admin.site.register(Badge, BadgeAdmin)    
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(ArticleHistoryItem)
admin.site.register(ArticleRatingItem)
admin.site.register(ArticleDifficultyItem)
admin.site.register(WordHistoryItem)
