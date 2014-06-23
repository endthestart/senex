from django.db import models
from django.utils.translation import ugettext_lazy as _


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

