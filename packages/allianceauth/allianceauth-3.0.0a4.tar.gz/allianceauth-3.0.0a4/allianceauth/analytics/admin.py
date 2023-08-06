from django.contrib import admin

from .models import AnalyticsIdentifier, AnalyticsPath, AnalyticsTokens


@admin.register(AnalyticsIdentifier)
class AnalyticsIdentifierAdmin(admin.ModelAdmin):
    search_fields = ['identifier', ]
    list_display = ('identifier',)


@admin.register(AnalyticsTokens)
class AnalyticsTokensAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ('name', 'type',)


@admin.register(AnalyticsPath)
class AnalyticsPathAdmin(admin.ModelAdmin):
    search_fields = ['ignore_path', ]
    list_display = ('ignore_path',)
