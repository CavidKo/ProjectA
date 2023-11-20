from modeltranslation.translator import translator, TranslationOptions
from core.models import *


class ClothesTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'category', 'color', 'tag', 'materials')

translator.register(Clothes, ClothesTranslationOptions)
