# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'OptionValue'
        db.delete_table(u'store_optionvalue')

        # Adding model 'ProductAttribute'
        db.create_table(u'store_productattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Product'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.AttributeOption'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'store', ['ProductAttribute'])

        # Adding model 'AttributeOption'
        db.create_table(u'store_attributeoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('validation', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('error_message', self.gf('django.db.models.fields.CharField')(default=u'invalid entry', max_length=100)),
        ))
        db.send_create_signal(u'store', ['AttributeOption'])

        # Adding field 'Option.value'
        db.add_column(u'store_option', 'value',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=50),
                      keep_default=False)

        # Adding field 'Option.price_change'
        db.add_column(u'store_option', 'price_change',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=2),
                      keep_default=False)


        # Changing field 'Option.name'
        db.alter_column(u'store_option', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Adding unique constraint on 'Option', fields ['option_group', 'value']
        db.create_unique(u'store_option', ['option_group_id', 'value'])

        # Deleting field 'Product.option_group'
        db.delete_column(u'store_product', 'option_group_id')

        # Adding field 'Product.sku'
        db.add_column(u'store_product', 'sku',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'Option', fields ['option_group', 'value']
        db.delete_unique(u'store_option', ['option_group_id', 'value'])

        # Adding model 'OptionValue'
        db.create_table(u'store_optionvalue', (
            ('price_change', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['store.Option'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='50')),
        ))
        db.send_create_signal(u'store', ['OptionValue'])

        # Deleting model 'ProductAttribute'
        db.delete_table(u'store_productattribute')

        # Deleting model 'AttributeOption'
        db.delete_table(u'store_attributeoption')

        # Deleting field 'Option.value'
        db.delete_column(u'store_option', 'value')

        # Deleting field 'Option.price_change'
        db.delete_column(u'store_option', 'price_change')


        # Changing field 'Option.name'
        db.alter_column(u'store_option', 'name', self.gf('django.db.models.fields.CharField')(max_length='50'))

        # User chose to not deal with backwards NULL issues for 'Product.option_group'
        raise RuntimeError("Cannot reverse this migration. 'Product.option_group' and its values cannot be restored.")
        # Deleting field 'Product.sku'
        db.delete_column(u'store_product', 'sku')


    models = {
        u'store.attributeoption': {
            'Meta': {'ordering': "('sort_order',)", 'object_name': 'AttributeOption'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'error_message': ('django.db.models.fields.CharField', [], {'default': "u'invalid entry'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'validation': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'store.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': u"orm['store.Category']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'related_categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_categories_rel_+'", 'null': 'True', 'to': u"orm['store.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'store.option': {
            'Meta': {'ordering': "('option_group', 'name')", 'unique_together': "(('option_group', 'value'),)", 'object_name': 'Option'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'option_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['store.OptionGroup']"}),
            'price_change': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'store.optiongroup': {
            'Meta': {'object_name': 'OptionGroup'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'store.product': {
            'Meta': {'ordering': "('ordering', 'name')", 'object_name': 'Product'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'category'", 'to': u"orm['store.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'stock': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '18', 'decimal_places': '6'})
        },
        u'store.productattribute': {
            'Meta': {'ordering': "('option__sort_order',)", 'object_name': 'ProductAttribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['store.AttributeOption']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['store.Product']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['store']