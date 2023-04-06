from django.contrib import admin

from .models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    """Для поиска по этим полям в админке"""
    search_fields = ('email', 'username')
