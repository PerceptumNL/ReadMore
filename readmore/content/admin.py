from django.contrib import admin
from readmore.content.models import *
from polymorphic.admin import PolymorphicParentModelAdmin, \
        PolymorphicChildModelAdmin

class WikiCategoryAdmin(PolymorphicChildModelAdmin):
    base_model = WikiCategory

class RegularCategoryAdmin(PolymorphicChildModelAdmin):
    base_model = Category

class CategoryAdmin(PolymorphicParentModelAdmin):
    base_model = Category
    child_models = (
        (WikiCategory, WikiCategoryAdmin),
        (Category, RegularCategoryAdmin)
    )

class WikiArticleAdmin(PolymorphicChildModelAdmin):
    base_model = WikiArticle

class RegularArticleAdmin(PolymorphicChildModelAdmin):
    base_model = Article

class ArticleAdmin(PolymorphicParentModelAdmin):
    base_model = Article
    child_models = (
        (WikiArticle, WikiArticleAdmin),
        (Article, RegularArticleAdmin)
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)

