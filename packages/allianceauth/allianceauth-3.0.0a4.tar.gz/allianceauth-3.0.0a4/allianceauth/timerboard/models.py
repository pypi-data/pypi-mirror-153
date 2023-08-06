from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from allianceauth.eveonline.models import EveCharacter
from allianceauth.eveonline.models import EveCorporationInfo


class TimerType(models.TextChoices):
    """
    Choices for Timer Type
    """

    UNSPECIFIED = "UNSPECIFIED", _("Not Specified")
    SHIELD = "SHIELD", _("Shield")
    ARMOR = "ARMOR", _("Armor")
    HULL = "HULL", _("Hull")
    FINAL = "FINAL", _("Final")
    ANCHORING = "ANCHORING", _("Anchoring")
    UNANCHORING = "UNANCHORING", _("Unanchoring")


class Timer(models.Model):
    class Meta:
        ordering = ['eve_time']

    details = models.CharField(max_length=254, default="")
    system = models.CharField(max_length=254, default="")
    planet_moon = models.CharField(max_length=254, default="")
    structure = models.CharField(max_length=254, default="")
    timer_type = models.CharField(
        max_length=254,
        choices=TimerType.choices,
        default=TimerType.UNSPECIFIED,
    )
    objective = models.CharField(max_length=254, default="")
    eve_time = models.DateTimeField()
    important = models.BooleanField(default=False)
    eve_character = models.ForeignKey(EveCharacter, null=True, on_delete=models.SET_NULL)
    eve_corp = models.ForeignKey(EveCorporationInfo, on_delete=models.CASCADE)
    corp_timer = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.system) + ' ' + str(self.details)
