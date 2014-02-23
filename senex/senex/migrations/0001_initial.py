# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table(u'senex_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('state', self.gf('localflavor.us.models.USStateField')(max_length=2)),
            ('zip_code', self.gf('localflavor.us.models.USPostalCodeField')(max_length=2)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'senex', ['Company'])

        # Adding model 'CustomBuild'
        db.create_table(u'senex_custombuild', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'senex', ['CustomBuild'])


    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table(u'senex_company')

        # Deleting model 'CustomBuild'
        db.delete_table(u'senex_custombuild')


    models = {
        u'senex.company': {
            'Meta': {'object_name': 'Company'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'zip_code': ('localflavor.us.models.USPostalCodeField', [], {'max_length': '2'})
        },
        u'senex.custombuild': {
            'Meta': {'object_name': 'CustomBuild'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['senex']