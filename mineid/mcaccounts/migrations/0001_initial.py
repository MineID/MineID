# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MinecraftAccount'
        db.create_table(u'mcaccounts_minecraftaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='minecraft_accounts', to=orm['accounts.User'])),
            ('profile', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('profile_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'mcaccounts', ['MinecraftAccount'])

        # Adding unique constraint on 'MinecraftAccount', fields ['user', 'primary']
        db.create_unique(u'mcaccounts_minecraftaccount', ['user_id', 'primary'])


    def backwards(self, orm):
        # Removing unique constraint on 'MinecraftAccount', fields ['user', 'primary']
        db.delete_unique(u'mcaccounts_minecraftaccount', ['user_id', 'primary'])

        # Deleting model 'MinecraftAccount'
        db.delete_table(u'mcaccounts_minecraftaccount')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'mcaccounts.minecraftaccount': {
            'Meta': {'unique_together': "(('user', 'primary'),)", 'object_name': 'MinecraftAccount'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'profile_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'minecraft_accounts'", 'to': u"orm['accounts.User']"})
        }
    }

    complete_apps = ['mcaccounts']