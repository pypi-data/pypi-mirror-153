from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from uuid import uuid4


class AnalyticsIdentifier(models.Model):

    identifier = models.UUIDField(default=uuid4,
                                  editable=False)

    def save(self, *args, **kwargs):
        if not self.pk and AnalyticsIdentifier.objects.exists():
            # Force a single object
            raise ValidationError('There is can be only one \
                                   AnalyticsIdentifier instance')
        self.pk = self.id = 1 # If this happens to be deleted and recreated, force it to be 1
        return super().save(*args, **kwargs)


class AnalyticsPath(models.Model):
    ignore_path = models.CharField(max_length=254, default="/example/", help_text="Regex Expression, If matched no Analytics Page View is sent")


class AnalyticsTokens(models.Model):

    class Analytics_Type(models.TextChoices):
        GA_U = 'GA-U', _('Google Analytics Universal')
        GA_V4 = 'GA-V4', _('Google Analytics V4')

    name = models.CharField(max_length=254)
    type = models.CharField(max_length=254, choices=Analytics_Type.choices)
    token = models.CharField(max_length=254, blank=False)
    send_page_views = models.BooleanField(default=False)
    send_celery_tasks = models.BooleanField(default=False)
    send_stats = models.BooleanField(default=False)
    ignore_paths = models.ManyToManyField(AnalyticsPath, blank=True)
