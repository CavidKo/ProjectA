from modeltranslation.translator import translator, TranslationOptions
from core.models import Clothes


class ClothesTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Clothes, ClothesTranslationOptions)


