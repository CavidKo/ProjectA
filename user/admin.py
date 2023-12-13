from django.contrib import admin
from user.models import MyUser

# Register your models here.

# @admin.register(MyUser)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ( 'email', )
#     autocomplete_fields = ('First name',)

admin.site.register(MyUser)
