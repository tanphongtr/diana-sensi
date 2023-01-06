from django.db import models
from django.utils.translation import ugettext_lazy as _

class TypeTextChoices(models.TextChoices):
    WET_MARKET = 'WET_MARKET', _('Wet Market')
    EXPERIENTIAL = 'EXPERIENTIAL', _('Experiential')