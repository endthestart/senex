# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('senex', '0002_galleryphoto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='galleryphoto',
            options={'verbose_name': 'gallery photo', 'verbose_name_plural': 'gallery photos'},
        ),
        migrations.AlterField(
            model_name='galleryphoto',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(help_text='The image associated with the promotion box.', upload_to=b'gallery', null=True, verbose_name='image', blank=True),
        ),
    ]
