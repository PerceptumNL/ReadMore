from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from longerusernameandemail.forms import UserCreationForm, UserChangeForm

from models import *

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    filter_horizontal = ('badges',)


class CustomUserAdmin(UserAdmin):
    save_on_top = True
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')
    inlines = [UserProfileInline]
    add_fieldsets = (
        ( None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )
    add_form = UserCreationForm
    form = UserChangeForm


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


class ArticleRatingItemAdmin(PolymorphicChildModelAdmin):
    base_model = ArticleRatingItem
    list_display = ('user', 'rating', 'article', 'date')


class ArticleDifficultyItemAdmin(PolymorphicChildModelAdmin):
    base_model = ArticleDifficultyItem
    list_display = ('user', 'rating', 'article', 'date')


class EventAdmin(PolymorphicParentModelAdmin):
    base_model = Event
    list_display = ('user', 'get_type', 'get_article', 'get_value', 'date')
    
    list_filter = (PolymorphicChildModelFilter,)
    child_models = (
        (ArticleHistoryItem, ArticleHistoryItemAdmin),
        (WordHistoryItem, WordHistoryItemAdmin),
        (ArticleRatingItem, ArticleRatingItemAdmin),
        (ArticleDifficultyItem, ArticleDifficultyItemAdmin)
    )

    def get_type(self, obj):
        crt_class = type(obj.get_real_instance()).__name__
        if crt_class=='ArticleHistoryItem':
            return "Read"
        elif crt_class=='WordHistoryItem':
            return "Clicked word"
        elif crt_class=='ArticleRatingItem':
            return "Rated Article"
        elif crt_class=='ArticleDifficultyItem':
            return "Rated Difficulty"
        else:
            return crt_class
    def get_article(self, obj):
        return str(obj.get_real_instance().article)
    get_article.short_description = 'Article'
    def get_value(self, obj):
        crt_class = type(obj.get_real_instance()).__name__
        if crt_class=='WordHistoryItem':
            return obj.get_real_instance().word
        elif crt_class=='ArticleRatingItem':
            return obj.get_real_instance().rating
        elif crt_class=='ArticleDifficultyItem':
            return obj.get_real_instance().rating
        else:
            return ""
    get_value.short_description = 'Value'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Institute)
admin.site.register(Group)
admin.site.register(Event, EventAdmin)
admin.site.register(UserProfile)