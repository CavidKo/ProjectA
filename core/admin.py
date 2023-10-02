from django.contrib import admin
from core.models import Contact, Categories, Clothes, Colors, Sizes

# Register your models here.

admin.site.register(Contact)
admin.site.register(Categories)
admin.site.register(Colors)
admin.site.register(Clothes)
admin.site.register(Sizes)
