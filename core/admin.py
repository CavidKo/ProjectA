from django.contrib import admin
from core.models import *

# Register your models here.

admin.site.register(Contact)
admin.site.register(Settings)
admin.site.register(Logo)
admin.site.register(CartProduct)
admin.site.register(Clothes)


# @admin.register(Clothes)
# class ClothesAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'active')
#     list_filter = ('category', 'active')
#     search_fields = ('name', 'price', 'category__category')
#     list_per_page = 10

#     fieldsets = (
#         ('Main', {
#             'fields': ('name', 'price', 'active')
#         }),
#         ('Advanced', {
#             'classes': ('collapse',),
#             'fields': ('description', 'category', 'size', 'tag', 'color', 'weight', 'length', 'width', 'height', 'materials', 'image', 'added_to_whishlist', 'slug')
#         })
#     )

#     autocomplete_fields = ('category', 'size', 'color', 'tag')




@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    autocomplete_fields = ('categories', 'tags',)


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category', )


@admin.register(BlogCategories)
class BlogCategoryAdmin(admin.ModelAdmin):
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

