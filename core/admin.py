import datetime
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from core.models import *

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _


from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)

# Register your models here.

##########################################

admin.site.register(Contact)
admin.site.register(Logo)
admin.site.register(Reviews)
admin.site.register(CozaStoreGallery)
admin.site.register(BlogComments)

@admin.register(CartProduct)
class CartProductAdmin(TranslationAdmin):
    search_fields = ()


@admin.register(About)
class AboutAdmin(TranslationAdmin):
    search_fields = ()


@admin.register(Settings)
class SettingsAdmin(TranslationAdmin):
    search_fields = ('adress', )

##########################################################
####################  Blogs #########################
##########################################################

@admin.register(BlogCategories)
class BlogCategoryAdmin(TranslationAdmin):
    search_fields = ('category', )


@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    search_fields = ('name',)
    autocomplete_fields = ('categories', 'tags',)


##########################################################
####################  Clothes #########################
##########################################################

class ClothesResource(resources.ModelResource):
    class Meta:
        model = Clothes
    

    def dehydrate_category(self, product):
        return product.category.category
        
    def dehydrate_active(self, product):
        return 'True' if product.active else 'False'
    
    def dehydrate_richtext(self, product):
        return strip_tags(product.description)


@admin.register(Clothes)
class ClothesAdmin(TranslationAdmin, ImportExportModelAdmin):
    resource_class = ClothesResource
    search_fields = ('name', 'price', 'category__category')
    autocomplete_fields = ('category', 'size', 'color', 'tag')
#    list_filter = ('active', 'category', 'create_time', 'update_time')
    list_filter = ('active', 'category',
        (
            "update_time",
            DateTimeRangeFilterBuilder(
                title=_('By date'),
                default_start=datetime.datetime(2020, 1, 1),
                default_end=datetime.datetime(2030, 1, 1),
            )
        ),
    )
    


@admin.register(Categories)
class CategoryAdmin(TranslationAdmin):
    search_fields = ('category', )


@admin.register(Sizes)
class SizeAdmin(TranslationAdmin):
    search_fields = ('size', )


@admin.register(Colors)
class ColorAdmin(TranslationAdmin):
    search_fields = ('color', )


@admin.register(Tags)
class TagsAdmin(TranslationAdmin):
    search_fields = ('tag', )

admin.site.site_header = 'Cozastore admin panel'

