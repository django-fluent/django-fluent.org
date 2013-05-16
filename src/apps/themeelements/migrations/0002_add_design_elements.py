# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContentBoxItem'
        db.create_table('contentitem_themeelements_contentboxitem', (
            ('contentitem_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fluent_contents.ContentItem'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('themeelements', ['ContentBoxItem'])

        # Adding model 'ImageTextItem'
        db.create_table('contentitem_themeelements_imagetextitem', (
            ('contentitem_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fluent_contents.ContentItem'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('image', self.gf('any_imagefield.models.fields.AnyImageField')(max_length=100)),
            ('body', self.gf('tinymce.models.HTMLField')()),
            ('url', self.gf('any_urlfield.models.fields.AnyUrlField')(max_length=300, blank=True)),
            ('url_text', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('themeelements', ['ImageTextItem'])

        # Adding model 'Col12Item'
        db.create_table('contentitem_themeelements_col12item', (
            ('contentitem_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fluent_contents.ContentItem'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('icon', self.gf('any_imagefield.models.fields.AnyImageField')(max_length=100, blank=True)),
            ('body', self.gf('tinymce.models.HTMLField')()),
        ))
        db.send_create_signal('themeelements', ['Col12Item'])


    def backwards(self, orm):
        # Deleting model 'ContentBoxItem'
        db.delete_table('contentitem_themeelements_contentboxitem')

        # Deleting model 'ImageTextItem'
        db.delete_table('contentitem_themeelements_imagetextitem')

        # Deleting model 'Col12Item'
        db.delete_table('contentitem_themeelements_col12item')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fluent_contents.contentitem': {
            'Meta': {'ordering': "('placeholder', 'sort_order')", 'object_name': 'ContentItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'parent_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contentitems'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['fluent_contents.Placeholder']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_fluent_contents.contentitem_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        'fluent_contents.placeholder': {
            'Meta': {'unique_together': "(('parent_type', 'parent_id', 'slot'),)", 'object_name': 'Placeholder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'parent_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'slot': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'themeelements.col12item': {
            'Meta': {'ordering': "('placeholder', 'sort_order')", 'object_name': 'Col12Item', 'db_table': "'contentitem_themeelements_col12item'", '_ormbases': ['fluent_contents.ContentItem']},
            'body': ('tinymce.models.HTMLField', [], {}),
            'contentitem_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fluent_contents.ContentItem']", 'unique': 'True', 'primary_key': 'True'}),
            'icon': ('any_imagefield.models.fields.AnyImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'themeelements.contentboxitem': {
            'Meta': {'ordering': "('placeholder', 'sort_order')", 'object_name': 'ContentBoxItem', 'db_table': "'contentitem_themeelements_contentboxitem'", '_ormbases': ['fluent_contents.ContentItem']},
            'contentitem_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fluent_contents.ContentItem']", 'unique': 'True', 'primary_key': 'True'})
        },
        'themeelements.imagetextitem': {
            'Meta': {'ordering': "('placeholder', 'sort_order')", 'object_name': 'ImageTextItem', 'db_table': "'contentitem_themeelements_imagetextitem'", '_ormbases': ['fluent_contents.ContentItem']},
            'body': ('tinymce.models.HTMLField', [], {}),
            'contentitem_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fluent_contents.ContentItem']", 'unique': 'True', 'primary_key': 'True'}),
            'image': ('any_imagefield.models.fields.AnyImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('any_urlfield.models.fields.AnyUrlField', [], {'max_length': '300', 'blank': 'True'}),
            'url_text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'themeelements.packageitem': {
            'Meta': {'ordering': "('slug',)", 'object_name': 'PackageItem', 'db_table': "'contentitem_themeelements_packageitem'", '_ormbases': ['fluent_contents.ContentItem']},
            'contentitem_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fluent_contents.ContentItem']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'repository_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'rtd_html_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['themeelements']