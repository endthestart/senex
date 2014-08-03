from django.db import models
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.fields import ThumbnailerImageField


class PromoBox(models.Model):
    ordering = models.IntegerField(
        _('ordering'),
        default=0,
        help_text=_("Override default alphabetical ordering"),
    )
    label = models.CharField(
        _('label'),
        max_length=25,
        default='',
        blank=True,
        help_text=_("The label for the promotion box."),
    )
    description = models.TextField(
        _('description'),
        max_length=255,
        default='',
        blank=True,
        help_text=_("Additional text that can be used for alt text, etc."),
    )
    image = ThumbnailerImageField(
        _("image"),
        upload_to='promobox',
        blank=True,
        null=True,
        help_text=_("The image associated with the promotion box."),
    )
    link = models.CharField(
        _('link'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The relevant content link for the promotion box."),
    )

    def __unicode__(self):
        return self.label

    class Meta:
        ordering = ('ordering', 'label')
        verbose_name = _("promo box")
        verbose_name_plural = _("promo boxes")


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

