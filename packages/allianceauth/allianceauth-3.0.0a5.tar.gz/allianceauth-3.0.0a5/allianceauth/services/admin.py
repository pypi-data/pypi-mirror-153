from django import forms
from django.contrib import admin

from allianceauth import hooks
from allianceauth.authentication.admin import (
    user_profile_pic,
    user_username,
    user_main_organization,
    MainCorporationsFilter,
    MainAllianceFilter
)

from .models import NameFormatConfig


class ServicesUserAdmin(admin.ModelAdmin):
    """Parent class for UserAdmin classes for all services"""
    class Media:
        css = {
            "all": ("services/admin.css",)
        }

    search_fields = ('user__username',)
    ordering = ('user__username',)
    list_select_related = True
    list_display = (
        user_profile_pic,
        user_username,
        '_state',
        user_main_organization,
        '_date_joined'
    )
    list_filter = (
        'user__profile__state',
        MainCorporationsFilter,
        MainAllianceFilter,
        'user__date_joined',
    )

    def _state(self, obj):
        return obj.user.profile.state.name

    _state.short_description = 'state'
    _state.admin_order_field = 'user__profile__state__name'

    def _date_joined(self, obj):
        return obj.user.date_joined

    _date_joined.short_description = 'date joined'
    _date_joined.admin_order_field = 'user__date_joined'


class NameFormatConfigForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        SERVICE_CHOICES = \
            [(s.name, s.name) for h in hooks.get_hooks('services_hook') for s in [h()]]
        if self.instance.id:
            current_choice = (self.instance.service_name, self.instance.service_name)
            if current_choice not in SERVICE_CHOICES:
                SERVICE_CHOICES.append(current_choice)
        self.fields['service_name'] = forms.ChoiceField(choices=SERVICE_CHOICES)


class NameFormatConfigAdmin(admin.ModelAdmin):
    form = NameFormatConfigForm
    list_display = ('service_name', 'get_state_display_string')

    def get_state_display_string(self, obj):
        return ', '.join([state.name for state in obj.states.all()])
    get_state_display_string.short_description = 'States'


admin.site.register(NameFormatConfig, NameFormatConfigAdmin)
