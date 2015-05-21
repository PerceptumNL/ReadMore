from django.contrib import admin
from readmore.content.models import *
from django_summernote.admin import SummernoteModelAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, \
        PolymorphicChildModelAdmin

class RSSCategoryAdmin(PolymorphicChildModelAdmin):
    base_model = RSSCategory

class SevenDaysCategoryAdmin(PolymorphicChildModelAdmin):
    base_model = SevenDaysCategory

class WikiCategoryAdmin(PolymorphicChildModelAdmin):
    base_model = WikiCategory

class RegularCategoryAdmin(PolymorphicChildModelAdmin):
    base_model = Category

class CategoryAdmin(PolymorphicParentModelAdmin):
    base_model = Category
    child_models = (
        (RSSCategory, RSSCategoryAdmin),
        (WikiCategory, WikiCategoryAdmin),
        (SevenDaysCategory, SevenDaysCategoryAdmin),
        (Category, RegularCategoryAdmin)
    )

class RSSArticleAdmin(PolymorphicChildModelAdmin):
    base_model = RSSArticle

class WikiArticleAdmin(PolymorphicChildModelAdmin):
    base_model = WikiArticle

class RegularArticleAdmin(PolymorphicChildModelAdmin, SummernoteModelAdmin):
    base_model = Article

class ArticleAdmin(PolymorphicParentModelAdmin):
    base_model = Article
    polymorphic_list = True
    search_fields = ['title',]
    list_display = ('title', 'main_category', 'publication_date',)
    list_filter = ('categories',)
    def main_category(self, obj):
        return obj.categories.first()
    def publication_date(self, obj):
        if(isinstance(obj, RSSArticle)):
            return obj.publication_date
        else:
            return " "
    
    
    
    child_models = (
        (RSSArticle, RSSArticleAdmin),
        (WikiArticle, WikiArticleAdmin),
        (Article, RegularArticleAdmin)
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)

