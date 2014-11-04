# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'main_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'main', ['UserProfile'])

        # Adding M2M table for field badges on 'UserProfile'
        m2m_table_name = db.shorten_name(u'main_userprofile_badges')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'main.userprofile'], null=False)),
            ('badge', models.ForeignKey(orm[u'main.badge'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'badge_id'])

        # Adding model 'Institute'
        db.create_table(u'main_institute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'main', ['Institute'])

        # Adding model 'Statistics'
        db.create_table(u'main_statistics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='statistics', unique=True, to=orm['auth.User'])),
            ('docsRead', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'main', ['Statistics'])

        # Adding model 'History'
        db.create_table(u'main_history', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('opened', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('article_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'main', ['History'])

        # Adding model 'Badge'
        db.create_table(u'main_badge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('default_image', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('field_to_listen_to', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'main', ['Badge'])

        # Adding model 'CounterBadge'
        db.create_table(u'main_counterbadge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='counter_badges', to=orm['main.Badge'])),
            ('trigger_at_greater_than', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['CounterBadge'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'main_userprofile')

        # Removing M2M table for field badges on 'UserProfile'
        db.delete_table(db.shorten_name(u'main_userprofile_badges'))

        # Deleting model 'Institute'
        db.delete_table(u'main_institute')

        # Deleting model 'Statistics'
        db.delete_table(u'main_statistics')

        # Deleting model 'History'
        db.delete_table(u'main_history')

        # Deleting model 'Badge'
        db.delete_table(u'main_badge')

        # Deleting model 'CounterBadge'
        db.delete_table(u'main_counterbadge')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'badges': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Badge']", 'symmetrical': 'False', 'blank': "'True'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['main']