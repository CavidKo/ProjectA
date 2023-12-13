from modeltranslation.translator import translator, TranslationOptions
from core.models import *


class ClothesTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'materials')

translator.register(Clothes, ClothesTranslationOptions)


class CategoriesTranslationOptions(TranslationOptions):
    fields = ('category',)

translator.register(Categories, CategoriesTranslationOptions)


class ColorsTranslationOptions(TranslationOptions):
    fields = ('color',)

translator.register(Colors, ColorsTranslationOptions)


class TagsTranslationOptions(TranslationOptions):
    fields = ('tag',)

translator.register(Tags, TagsTranslationOptions)


class SizesTranslationOptions(TranslationOptions):
    fields = ('size',)

translator.register(Sizes, SizesTranslationOptions)


class BlogTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

translator.register(Blog, BlogTranslationOptions)


class BlogCategoriesTranslationoptions(TranslationOptions):
        fields = ('category',)

translator.register(BlogCategories, BlogCategoriesTranslationoptions)


class SettingsTranslationOptions(TranslationOptions):
    fields = ('adress', 'info')

translator.register(Settings, SettingsTranslationOptions)


class AboutTranslationOptions(TranslationOptions):
    fields = ('our_story_text', 'our_mission_text')

translator.register(About, AboutTranslationOptions)


class CartProductsTranslationOptions(TranslationOptions):
    fields = ('size', 'color')

translator.register(CartProduct, CartProductsTranslationOptions)
