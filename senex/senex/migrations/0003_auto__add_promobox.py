# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PromoBox'
        db.create_table(u'senex_promobox', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('label', self.gf('django.db.models.fields.TextField')(default='', max_length=25, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', max_length=255, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'senex', ['PromoBox'])


    def backwards(self, orm):
        # Deleting model 'PromoBox'
        db.delete_table(u'senex_promobox')


    models = {
        u'senex.custombuild': {
            'Meta': {'object_name': 'CustomBuild'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'senex.promobox': {
            'Meta': {'ordering': "('ordering', 'label')", 'object_name': 'PromoBox'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '25', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['senex']