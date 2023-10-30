from django.contrib import admin
from core.models import *

# Register your models here.

admin.site.register(Contact)
admin.site.register(Settings)
admin.site.register(Logo)


@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'active')
    list_filter = ('category', 'active')
    search_fields = ('name', 'price', 'category__category')
    list_per_page = 10

    fieldsets = (
        ('Main', {
            'fields': ('name', 'price', 'active')
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('description', 'category', 'size', 'color', 'image', 'added_to_whishlist', 'slug')
        })
    )

    autocomplete_fields = ('category', 'size', 'color')


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category', )


@admin.register(Sizes)
class SizeAdmin(admin.ModelAdmin):
    search_fields = ('size', )


@admin.register(Colors)
class ColorAdmin(admin.ModelAdmin):
    search_fields = ('color', )

admin.site.site_header = 'Cozastore admin panel'

