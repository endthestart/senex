# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('senex', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', help_text='The title for the picture.', max_length=25, verbose_name='title', blank=True)),
                ('description', models.TextField(default=b'', help_text='Description of the image.', max_length=255, verbose_name='description', blank=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(help_text='The image associated with the promotion box.', upload_to=b'promobox', null=True, verbose_name='image', blank=True)),
            ],
        ),
    ]
