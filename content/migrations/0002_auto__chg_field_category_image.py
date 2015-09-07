# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field categories on 'Article'
        m2m_table_name = db.shorten_name(u'content_article_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'content.article'], null=False)),
            ('category', models.ForeignKey(orm[u'content.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'category_id'])


        # Changing field 'Category.image'
        db.alter_column(u'content_category', 'image', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):
        # Removing M2M table for field categories on 'Article'
        db.delete_table(db.shorten_name(u'content_article_categories'))


        # Changing field 'Category.image'
        db.alter_column(u'content_category', 'image', self.gf('django.db.models.fields.URLField')(max_length=255, null=True))

    models = {
        u'content.article': {
            'Meta': {'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'articles'", 'symmetrical': 'False', 'to': u"orm['content.Category']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['content.Category']"}),
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