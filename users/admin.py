from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ('email',)
    list_display = ('email', 'name', 'surname', 'is_staff', 'is_active')
    search_fields = ('email', 'name', 'surname')
    filter_horizontal = ('favorites', 'groups', 'user_permissions')
    readonly_fields = ('last_login', 'date_joined')
