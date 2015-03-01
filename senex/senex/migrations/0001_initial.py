# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomBuild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(help_text='The type of customization.', max_length=128, verbose_name='custom type')),
                ('description', models.TextField(help_text='The customization description.', verbose_name='description')),
            ],
            options={
                'verbose_name': 'custom build',
                'verbose_name_plural': 'custom builds',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PromoBox',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField(default=0, help_text='Override default alphabetical ordering', verbose_name='ordering')),
                ('label', models.CharField(default=b'', help_text='The label for the promotion box.', max_length=25, verbose_name='label', blank=True)),
                ('description', models.TextField(default=b'', help_text='Additional text that can be used for alt text, etc.', max_length=255, verbose_name='description', blank=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(help_text='The image associated with the promotion box.', upload_to=b'promobox', null=True, verbose_name='image', blank=True)),
                ('link', models.CharField(help_text='The relevant content link for the promotion box.', max_length=255, null=True, verbose_name='link', blank=True)),
            ],
            options={
                'ordering': ('ordering', 'label'),
                'verbose_name': 'promo box',
                'verbose_name_plural': 'promo boxes',
            },
            bases=(models.Model,),
        ),
    ]
