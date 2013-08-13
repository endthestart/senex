from django.db import models

from django.utils.translation import ugettext_lazy as _
from django_localflavor_us.models import USStateField, USPostalCodeField


class Address(models.Model):
    address_1 = models.CharField(
        _("address"),
        max_length=128,
        help_text=_('Address 1'),
    )
    address_2 = models.CharField(
        _("additional address"),
        max_length=128,
        blank=True,
        help_text=_('Address 2'),
        )
    city = models.CharField(
        _("city"),
        max_length=64,
        help_text=_('City'),
    )
    state = USStateField(
        _("state"),
        help_text=_('State'),
    )
    zip_code = USPostalCodeField(
        _("zip code"),
        max_length=5,
        help_text=_('Zip Code'),
    )

    class Meta:
        abstract = True