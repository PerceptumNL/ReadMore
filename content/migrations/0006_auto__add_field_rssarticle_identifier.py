# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RSSArticle.identifier'
        db.add_column(u'content_rssarticle', 'identifier',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RSSArticle.identifier'
        db.delete_column(u'content_rssarticle', 'identifier')


    models = {
        u'content.article': {
            'Meta': {'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'articles'", 'symmetrical': 'False', 'to': u"orm['content.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_content.article_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'content.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['content.Category']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_content.category_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'content.rssarticle': {
            'Meta': {'object_name': 'RSSArticle', '_ormbases': [u'content.Article']},
            u'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['content.Article']", 'unique': 'True', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'content.rsscategory': {
            'Meta': {'object_name': 'RSSCategory', '_ormbases': [u'content.Category']},
            u'category_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['content.Category']", 'unique': 'True', 'primary_key': 'True'}),
            'feed': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'content.wikiarticle': {
            'Meta': {'object_name': 'WikiArticle', '_ormbases': [u'content.Article']},
            u'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['content.Article']", 'unique': 'True', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'identifier_type': ('django.db.models.fields.CharField', [], {'default': "'title'", 'max_length': '6', 'blank': 'True'})
        },
        u'content.wikicategory': {
            'Meta': {'object_name': 'WikiCategory', '_ormbases': [u'content.Category']},
            u'category_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['content.Category']", 'unique': 'True', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'identifier_type': ('django.db.models.fields.CharField', [], {'default': "'title'", 'max_length': '6', 'blank': 'True'}),
            'wiki_type': ('django.db.models.fields.CharField', [], {'default': "'14'", 'max_length': '3'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['content']