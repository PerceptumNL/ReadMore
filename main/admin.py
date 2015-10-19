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
    list_display = ('email', 'full_name', 'date_joined',
            'last_login', 'num_active', "teacher_dashboard")
    list_filter = ('userprofile__institute','userprofile__is_teacher')
    inlines = [UserProfileInline]
    add_fieldsets = (
        ( None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )
    add_form = UserCreationForm
    form = UserChangeForm

    def full_name(self, obj):
        return obj.get_full_name()

    def num_active(self, obj):
        if not obj.userprofile.is_teacher:
            return "n/a"
        from datetime import timedelta, date
        profiles = UserProfile.objects.filter(groups__leader__pk=obj.pk)
        compare_date = date.today()-timedelta(weeks=1)
        compare_date_before = compare_date-timedelta(weeks=1)
        total = 0
        active = 0
        active_before = 0
        for profile in profiles:
            if not profile.is_teacher:
                total += 1
                if Event.objects.filter(user=profile.user,
                        date__gt=compare_date).exists():
                    active += 1
                if Event.objects.filter(user=profile.user,
                        date__gt=compare_date_before,
                        date__lt=compare_date).exists():
                    active_before += 1

        if active > active_before:
            direction = "&#9650;"
        elif active_before > active:
            direction = "&#9660;"
        else:
            direction = "&#x26AB;"
        return "%d / %d in the last week (%s)" % (active, total, direction)
    num_active.allow_tags = True

    def teacher_dashboard(self, obj):
        if not obj.userprofile.is_teacher:
            return "n/a"
        else:
            link = "%s?teacher=%d" % (reverse("dashboard_dispatch"), obj.pk)
            return "<a href='%s'>Dashboard</a>" % (link,)
    teacher_dashboard.allow_tags = True



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

class PilotSignupAdmin(admin.ModelAdmin):
    base_model = PilotSignup
    list_filter = ('function', 'school')
    list_display = ('email', 'function', 'school', 'signup',)

class InstituteModel(admin.ModelAdmin):
    list_display = ('title', 'num_active', 'teachers_link')

    def num_active(self, obj):
        from datetime import timedelta, date
        profiles = UserProfile.objects.filter(institute__pk=obj.pk)
        compare_date = date.today()-timedelta(weeks=1)
        compare_date_before = compare_date-timedelta(weeks=1)
        total = 0
        active = 0
        active_before = 0
        for profile in profiles:
            if not profile.is_teacher:
                total += 1
                if Event.objects.filter(user=profile.user,
                        date__gt=compare_date).exists():
                    active += 1
                if Event.objects.filter(user=profile.user,
                        date__gt=compare_date_before,
                        date__lt=compare_date).exists():
                    active_before += 1

        if active > active_before:
            direction = "&#9650;"
        elif active_before > active:
            direction = "&#9660;"
        else:
            direction = "&#x26AB;"
        return "%d / %d in the last week (%s)" % (active, total, direction)
    num_active.allow_tags = True

    def teachers_link(self, obj):
        from django.contrib.auth import get_user_model
        model = get_user_model()
        info = model._meta.app_label, model._meta.model_name
        link = ("%s?userprofile__institute__id__exact=%d" +
                "&userprofile__is_teacher__exact=1") % (
                reverse('admin:%s_%s_changelist' % info), obj.pk)
        return "<a href='%s'>Docenten</a>" % (link,)
    teachers_link.allow_tags = True

class TeacherCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'institute', 'created_on', 'users')

    def users(self, obj):
        return UserProfile.objects.filter(code__pk=obj.pk).count()

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Institute, InstituteModel)
admin.site.register(Group)
admin.site.register(TeacherCode, TeacherCodeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(UserProfile)
admin.site.register(PilotSignup, PilotSignupAdmin)
