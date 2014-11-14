from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, \
        PolymorphicChildModelAdmin
from models import *

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


class WordHistoryItemAdmin(PolymorphicChildModelAdmin):
    base_model = WordHistoryItem
    list_display = ('user', 'word', 'article', 'date')


class ArticleHistoryItemAdmin(PolymorphicChildModelAdmin):
    base_model = ArticleHistoryItem
    list_display = ('user', 'article', 'date')


class ArticleRatingItemAdmin(admin.ModelAdmin):
    base_model = ArticleRatingItem
    list_display = ('user', 'rating', 'article', 'date')


class ArticleDifficultyItemAdmin(admin.ModelAdmin):
    base_model = ArticleDifficultyItem
    list_display = ('user', 'rating', 'article', 'date')


class EventAdmin(PolymorphicParentModelAdmin):
    base_model = Event
    child_models = (
        (ArticleHistoryItem, ArticleHistoryItemAdmin),
        (WordHistoryItem, WordHistoryItemAdmin),
        (ArticleRatingItem, ArticleRatingItemAdmin),
        (ArticleDifficultyItem, ArticleDifficultyItemAdmin)
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Institute)
admin.site.register(Group)
admin.site.register(Event, EventAdmin)
