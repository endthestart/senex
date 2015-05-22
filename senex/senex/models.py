from django.db import models
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.fields import ThumbnailerImageField


class PromoBox(models.Model):
    ordering = models.IntegerField(
        _(u'ordering'),
        default=0,
        help_text=_(u"Override default alphabetical ordering"),
    )
    label = models.CharField(
        _(u'label'),
        max_length=25,
        default='',
        blank=True,
        help_text=_(u"The label for the promotion box."),
    )
    description = models.TextField(
        _(u'description'),
        max_length=255,
        default='',
        blank=True,
        help_text=_(u"Additional text that can be used for alt text, etc."),
    )
    image = ThumbnailerImageField(
        _(u"image"),
        upload_to='promobox',
        blank=True,
        null=True,
        help_text=_(u"The image associated with the promotion box."),
    )
    link = models.CharField(
        _(u'link'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_(u"The relevant content link for the promotion box."),
    )

    def save(self, *args, **kwargs):
        if self.ordering is None:
            self.ordering = self.next_available_order()

        try:
            dup_boxes = PromoBox.objects.filter(ordering__gte=self.ordering)
            for dup_box in dup_boxes:
                dup_box.ordering += 1
                dup_box.save()
        except PromoBox.DoesNotExist:
            pass
        super(PromoBox, self).save(*args, **kwargs)

    def next_available_order(self):
        try:
            order = max(PromoBox.objects.values_list('ordering', flat=True)) + 1
        except ValueError:
            order = 0
        return order

    def __unicode__(self):
        return self.label

    class Meta:
        ordering = ('ordering', 'label')
        verbose_name = _(u"promo box")
        verbose_name_plural = _(u"promo boxes")


class GalleryPhoto(models.Model):
    title = models.CharField(
        _(u'title'),
        max_length=25,
        default='',
        blank=True,
        help_text=_(u"The title for the picture."),
    )
    description = models.TextField(
        _(u'description'),
        max_length=255,
        default='',
        blank=True,
        help_text=_(u"Description of the image."),
    )
    image = ThumbnailerImageField(
        _(u"image"),
        upload_to='gallery',
        blank=True,
        null=True,
        help_text=_(u"The image associated with the promotion box."),
    )

    def image_tag(self):
        from easy_thumbnails.files import get_thumbnailer
        options = {'size': (75, 75)}
        thumb_url = get_thumbnailer(self.image).get_thumbnail(options).url
        return u'<img src="%s" />' % thumb_url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u"gallery photo")
        verbose_name_plural = _(u"gallery photos")

class CustomBuild(models.Model):
    type = models.CharField(
        _(u'custom type'),
        max_length=128,
        help_text=_(u"The type of customization."),
    )
    description = models.TextField(
        _(u'description'),
        help_text=_(u"The customization description."),
    )

    class Meta:
        verbose_name = _(u"custom build")
        verbose_name_plural = _(u"custom builds")

