from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_admin')
    list_filter = ('is_admin',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(MyUser, UserAdmin)
