from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django_localflavor_us.models import USStateField, USPostalCodeField, PhoneNumberField


class Company(models.Model):
    name = models.CharField(
        _('name'),
        max_length=128,
        help_text=_('The name of the company.'),
    )
    logo = models.ImageField(
        _('logo'),
        upload_to='logos',
        help_text=_('The company logo.'),
    )
    address = models.ForeignKey(
        'address',
        help_text=_('The address of the company.'),
    )
    phone = PhoneNumberField(
        _('phone'),
        help_text=_('The phone number of the company.'),
    )
    email = models.EmailField(
        _('email'),
        help_text=_('The contact number of the company.'),
    )


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

class Custom(models.Model):
    type = models.CharField(
        _('custom type'),
        max_length=128,
        help_text=('The type of customization.'),
    )
    description = models.TextField(
        _('description'),
        help_text=('The customization description.'),
    )
