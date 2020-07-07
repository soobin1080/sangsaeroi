from django.contrib import admin

from .models import User

# from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AdminUser(admin.ModelAdmin):

    list_display = ['email', 'nickname','is_admin','is_active',]

    list_editable = ['is_admin']

admin.site.register(User,AdminUser)