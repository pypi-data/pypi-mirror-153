from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .models import ReservedGroupName


class GroupAdminForm(forms.ModelForm):
    def clean_name(self):
        my_name = self.cleaned_data['name']
        if ReservedGroupName.objects.filter(name__iexact=my_name).exists():
            raise ValidationError(
                _("This name has been reserved and can not be used for groups."),
                code='reserved_name'
            )
        return my_name


class ReservedGroupNameAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by'].initial = self.current_user.username
        self.fields['created_at'].initial = _("(auto)")

    created_by = forms.CharField(disabled=True)
    created_at = forms.CharField(disabled=True)

    def clean_name(self):
        my_name = self.cleaned_data['name'].lower()
        if Group.objects.filter(name__iexact=my_name).exists():
            raise ValidationError(
                _("There already exists a group with that name."), code='already_exists'
            )
        return my_name

    def clean_created_at(self):
        return now()
