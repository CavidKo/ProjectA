from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from core.models import *

# Register your models here.

admin.site.register(Contact)
admin.site.register(Logo)
admin.site.register(CartProduct)


@admin.register(Settings)
class SettingsAdmin(TranslationAdmin):
    search_fields = ('adress', )

##########################################################
####################  Blogs #########################
##########################################################

@admin.register(BlogCategories)
class BlogCategoryAdmin(admin.ModelAdmin):
    search_fields = ('category', )


@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    search_fields = ('name',)
    autocomplete_fields = ('categories', 'tags',)


##########################################################
####################  Clothes #########################
##########################################################

@admin.register(Clothes)
class ClothesAdmin(TranslationAdmin):
    search_fields = ('name', 'price', 'category__category')
    autocomplete_fields = ('category', 'size', 'color', 'tag')


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category', )


@admin.register(Sizes)
class SizeAdmin(admin.ModelAdmin):
    search_fields = ('size', )


@admin.register(Colors)
class ColorAdmin(admin.ModelAdmin):
    search_fields = ('color', )


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    search_fields = ('tag', )

admin.site.site_header = 'Cozastore admin panel'

