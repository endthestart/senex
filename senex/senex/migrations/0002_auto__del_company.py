# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Company'
        db.delete_table(u'senex_company')


    def backwards(self, orm):
        # Adding model 'Company'
        db.create_table(u'senex_company', (
            ('phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('state', self.gf('localflavor.us.models.USStateField')(max_length=2)),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('zip_code', self.gf('localflavor.us.models.USPostalCodeField')(max_length=2)),
        ))
        db.send_create_signal(u'senex', ['Company'])


    models = {
        u'senex.custombuild': {
            'Meta': {'object_name': 'CustomBuild'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['senex']