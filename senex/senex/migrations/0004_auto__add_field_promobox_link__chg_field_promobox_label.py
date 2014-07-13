# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PromoBox.link'
        db.add_column(u'senex_promobox', 'link',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)


        # Changing field 'PromoBox.label'
        db.alter_column(u'senex_promobox', 'label', self.gf('django.db.models.fields.CharField')(max_length=25))

    def backwards(self, orm):
        # Deleting field 'PromoBox.link'
        db.delete_column(u'senex_promobox', 'link')


        # Changing field 'PromoBox.label'
        db.alter_column(u'senex_promobox', 'label', self.gf('django.db.models.fields.TextField')(max_length=25))

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
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['senex']