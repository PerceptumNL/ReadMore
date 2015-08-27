# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'content_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'polymorphic_content.category_set', null=True, to=orm['contenttypes.ContentType'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['content.Category'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'content', ['Category'])

        # Adding model 'WikiCategory'
        db.create_table(u'content_wikicategory', (
            (u'category_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['content.Category'], unique=True, primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('identifier_type', self.gf('django.db.models.fields.CharField')(default='title', max_length=6, blank=True)),
            ('wiki_type', self.gf('django.db.models.fields.CharField')(default='14', max_length=3)),
        ))
        db.send_create_signal(u'content', ['WikiCategory'])

        # Adding model 'Article'
        db.create_table(u'content_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'polymorphic_content.article_set', null=True, to=orm['contenttypes.ContentType'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['content.Category'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'content', ['Article'])

        # Adding model 'WikiArticle'
        db.create_table(u'content_wikiarticle', (
            (u'article_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['content.Article'], unique=True, primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('identifier_type', self.gf('django.db.models.fields.CharField')(default='title', max_length=6, blank=True)),
        ))
        db.send_create_signal(u'content', ['WikiArticle'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'content_category')

        # Deleting model 'WikiCategory'
        db.delete_table(u'content_wikicategory')

        # Deleting model 'Article'
        db.delete_table(u'content_article')

        # Deleting model 'WikiArticle'
        db.delete_table(u'content_wikiarticle')


    models = {
        u'content.article': {
            'Meta': {'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': u"orm['content.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_content.article_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'content.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['content.Category']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_content.category_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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