# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Ticket'
        db.create_table('tickets_ticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ticket_creator', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('context', self.gf('django.db.models.fields.CharField')(default='ct_repository_field_1', max_length=256)),
            ('type', self.gf('django.db.models.fields.CharField')(default='review', max_length=256)),
        ))
        db.send_create_signal('tickets', ['Ticket'])

        # Adding model 'Followup'
        db.create_table('tickets_followup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tickets.Ticket'])),
            ('iteration_date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('reported_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ticket_reported_by', null=True, to=orm['auth.User'])),
            ('to_user', self.gf('django.db.models.fields.EmailField')(db_index=True, max_length=256, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=256, db_index=True)),
        ))
        db.send_create_signal('tickets', ['Followup'])

        # Adding model 'Media'
        db.create_table('tickets_media', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('followup', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ticket_media', null=True, to=orm['tickets.Followup'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('tickets', ['Media'])


    def backwards(self, orm):
        
        # Deleting model 'Ticket'
        db.delete_table('tickets_ticket')

        # Deleting model 'Followup'
        db.delete_table('tickets_followup')

        # Deleting model 'Media'
        db.delete_table('tickets_media')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tickets.followup': {
            'Meta': {'object_name': 'Followup'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'reported_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ticket_reported_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '256', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tickets.Ticket']"}),
            'to_user': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'tickets.media': {
            'Meta': {'object_name': 'Media'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'followup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ticket_media'", 'null': 'True', 'to': "orm['tickets.Followup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tickets.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'context': ('django.db.models.fields.CharField', [], {'default': "'ct_repository_field_1'", 'max_length': '256'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ticket_creator'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'review'", 'max_length': '256'})
        }
    }

    complete_apps = ['tickets']
