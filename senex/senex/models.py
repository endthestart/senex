from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from localflavor.us.models import PhoneNumberField

from core.models import Address


class Company(Address):
    name = models.CharField(
        _('name'),
        max_length=128,
        help_text=_("The name of the company."),
    )
    logo = models.ImageField(
        _('logo'),
        upload_to='logos',
        help_text=_('The company logo.'),
    )
    phone = PhoneNumberField(
        _('phone'),
        help_text=_("The phone number of the company."),
    )
    email = models.EmailField(
        _('email'),
        help_text=_("The contact number of the company."),
    )

    class Meta:
        verbose_name = _("company")
        verbose_name_plural = _("companies")


class CustomBuild(models.Model):
    type = models.CharField(
        _('custom type'),
        max_length=128,
        help_text=_("The type of customization."),
    )
    description = models.TextField(
        _('description'),
        help_text=_("The customization description."),
    )

    class Meta:
        verbose_name = _("custom build")
        verbose_name_plural = _("custom builds")

