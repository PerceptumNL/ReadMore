# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'main_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'polymorphic_main.event_set', null=True, to=orm['contenttypes.ContentType'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Event'])

        # Deleting field 'WordHistoryItem.user'
        db.delete_column(u'main_wordhistoryitem', 'user_id')

        # Deleting field 'WordHistoryItem.date'
        db.delete_column(u'main_wordhistoryitem', 'date')

        # Deleting field 'WordHistoryItem.id'
        db.delete_column(u'main_wordhistoryitem', u'id')

        # Adding field 'WordHistoryItem.event_ptr'
        db.add_column(u'main_wordhistoryitem', u'event_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['main.Event'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ArticleDifficultyItem.user'
        db.delete_column(u'main_articledifficultyitem', 'user_id')

        # Deleting field 'ArticleDifficultyItem.date'
        db.delete_column(u'main_articledifficultyitem', 'date')

        # Deleting field 'ArticleDifficultyItem.id'
        db.delete_column(u'main_articledifficultyitem', u'id')

        # Adding field 'ArticleDifficultyItem.event_ptr'
        db.add_column(u'main_articledifficultyitem', u'event_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['main.Event'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ArticleHistoryItem.date'
        db.delete_column(u'main_articlehistoryitem', 'date')

        # Deleting field 'ArticleHistoryItem.id'
        db.delete_column(u'main_articlehistoryitem', u'id')

        # Deleting field 'ArticleHistoryItem.user'
        db.delete_column(u'main_articlehistoryitem', 'user_id')

        # Adding field 'ArticleHistoryItem.event_ptr'
        db.add_column(u'main_articlehistoryitem', u'event_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['main.Event'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ArticleRatingItem.user'
        db.delete_column(u'main_articleratingitem', 'user_id')

        # Deleting field 'ArticleRatingItem.date'
        db.delete_column(u'main_articleratingitem', 'date')

        # Deleting field 'ArticleRatingItem.id'
        db.delete_column(u'main_articleratingitem', u'id')

        # Adding field 'ArticleRatingItem.event_ptr'
        db.add_column(u'main_articleratingitem', u'event_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['main.Event'], unique=True, primary_key=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'main_event')


        # User chose to not deal with backwards NULL issues for 'WordHistoryItem.user'
        raise RuntimeError("Cannot reverse this migration. 'WordHistoryItem.user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'WordHistoryItem.user'
        db.add_column(u'main_wordhistoryitem', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'WordHistoryItem.date'
        raise RuntimeError("Cannot reverse this migration. 'WordHistoryItem.date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'WordHistoryItem.date'
        db.add_column(u'main_wordhistoryitem', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'WordHistoryItem.id'
        raise RuntimeError("Cannot reverse this migration. 'WordHistoryItem.id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'WordHistoryItem.id'
        db.add_column(u'main_wordhistoryitem', u'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)

        # Deleting field 'WordHistoryItem.event_ptr'
        db.delete_column(u'main_wordhistoryitem', u'event_ptr_id')


        # User chose to not deal with backwards NULL issues for 'ArticleDifficultyItem.user'
        raise RuntimeError("Cannot reverse this migration. 'ArticleDifficultyItem.user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ArticleDifficultyItem.user'
        db.add_column(u'main_articledifficultyitem', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ArticleDifficultyItem.date'
        raise RuntimeError("Cannot reverse this migration. 'ArticleDifficultyItem.date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ArticleDifficultyItem.date'
        db.add_column(u'main_articledifficultyitem', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ArticleDifficultyItem.id'
        raise RuntimeError("Cannot reverse this migration. 'ArticleDifficultyItem.id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ArticleDifficultyItem.id'
        db.add_column(u'main_articledifficultyitem', u'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)

        # Deleting field 'ArticleDifficultyItem.event_ptr'
        db.delete_column(u'main_articledifficultyitem', u'event_ptr_id')


        # User chose to not deal with backwards NULL issues for 'ArticleHistoryItem.date'
        raise RuntimeError("Cannot reverse this migration. 'ArticleHistoryItem.date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ArticleHistoryItem.date'
        db.add_column(u'main_articlehistoryitem', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ArticleHistoryItem.id'
        raise RuntimeError("Cannot reverse this migration. 'ArticleHistoryItem.id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ArticleHistoryItem.id'
        db.add_column(u'main_articlehistoryitem', u'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ArticleHistoryItem.user'
        raise RuntimeError("Cannot reverse this migration. 'ArticleHistoryItem.user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ArticleHistoryItem.user'
        db.add_column(u'main_articlehistoryitem', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'ArticleHistoryItem.event_ptr'
        db.delete_column(u'main_articlehistoryitem', u'event_ptr_id')


        # User chose to not deal with backwards NULL issues for 'ArticleRatingItem.user'
        raise RuntimeError("Cannot reverse this migration. 'ArticleRatingItem.user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ArticleRatingItem.user'
        db.add_column(u'main_articleratingitem', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ArticleRatingItem.date'
        raise RuntimeError("Cannot reverse this migration. 'ArticleRatingItem.date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ArticleRatingItem.date'
        db.add_column(u'main_articleratingitem', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ArticleRatingItem.id'
        raise RuntimeError("Cannot reverse this migration. 'ArticleRatingItem.id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ArticleRatingItem.id'
        db.add_column(u'main_articleratingitem', u'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)

        # Deleting field 'ArticleRatingItem.event_ptr'
        db.delete_column(u'main_articleratingitem', u'event_ptr_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'content.article': {
            'Meta': {'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'articles'", 'symmetrical': 'False', 'to': u"orm['content.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_content.article_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'content.category': {
            'Meta': {'object_name': 'Category'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'#f3f3f3'", 'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['content.Category']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_content.category_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.articledifficultyitem': {
            'Meta': {'ordering': "['-date']", 'object_name': 'ArticleDifficultyItem', '_ormbases': [u'main.Event']},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Article']"}),
            u'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {})
        },
        u'main.articlehistoryitem': {
            'Meta': {'ordering': "['-date']", 'object_name': 'ArticleHistoryItem', '_ormbases': [u'main.Event']},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Article']"}),
            u'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'main.articleratingitem': {
            'Meta': {'ordering': "['-date']", 'object_name': 'ArticleRatingItem', '_ormbases': [u'main.Event']},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Article']"}),
            u'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {})
        },
        u'main.badge': {
            'Meta': {'object_name': 'Badge'},
            'default_image': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'field_to_listen_to': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.counterbadge': {
            'Meta': {'ordering': "('trigger_at_greater_than',)", 'object_name': 'CounterBadge'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'counter_badges'", 'to': u"orm['main.Badge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'trigger_at_greater_than': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'main.event': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_main.event_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Institute']", 'null': 'True', 'blank': 'True'}),
            'leader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.history': {
            'Meta': {'object_name': 'History'},
            'article_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opened': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.institute': {
            'Meta': {'object_name': 'Institute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'site_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.statistics': {
            'Meta': {'object_name': 'Statistics'},
            'docsRead': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'statistics'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'badges': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'users'", 'blank': 'True', 'to': u"orm['main.Badge']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'users'", 'blank': 'True', 'to': u"orm['main.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'users'", 'null': 'True', 'to': u"orm['main.Institute']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'main.wordhistoryitem': {
            'Meta': {'ordering': "['-date']", 'object_name': 'WordHistoryItem', '_ormbases': [u'main.Event']},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Article']"}),
            u'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['main.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['main']