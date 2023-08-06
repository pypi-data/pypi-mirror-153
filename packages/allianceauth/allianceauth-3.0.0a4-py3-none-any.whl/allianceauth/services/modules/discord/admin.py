import logging

from django.contrib import admin

from . import __title__
from ...admin import ServicesUserAdmin
from .models import DiscordUser
from .utils import LoggerAddTag


logger = LoggerAddTag(logging.getLogger(__name__), __title__)


@admin.register(DiscordUser)
class DiscordUserAdmin(ServicesUserAdmin):
    search_fields = ServicesUserAdmin.search_fields + ('uid', 'username')
    list_display = ServicesUserAdmin.list_display + ('activated', '_username', '_uid')
    list_filter = ServicesUserAdmin.list_filter + ('activated',)
    ordering = ('-activated',)

    def _uid(self, obj):
        return obj.uid

    _uid.short_description = 'Discord ID (UID)'
    _uid.admin_order_field = 'uid'

    def _username(self, obj):
        if obj.username and obj.discriminator:
            return f'{obj.username}#{obj.discriminator}'
        else:
            return ''

    def delete_queryset(self, request, queryset):
        for user in queryset:
            user.delete_user()

    _username.short_description = 'Discord Username'
    _username.admin_order_field = 'username'
