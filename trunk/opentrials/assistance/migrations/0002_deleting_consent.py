# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_table('assistance_consent')
        db.delete_table('assistance_consenttranslation')


    def backwards(self, orm):
        pass


    models = {
        'assistance.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'assistance.categorytranslation': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'language'),)", 'object_name': 'CategoryTranslation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'assistance.fieldhelp': {
            'Meta': {'ordering': "('id',)", 'unique_together': "(('form', 'field'),)", 'object_name': 'FieldHelp'},
            'example': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'form': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '2048', 'blank': 'True'})
        },
        'assistance.fieldhelptranslation': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'language'),)", 'object_name': 'FieldHelpTranslation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'example': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '2048', 'blank': 'True'})
        },
        'assistance.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assistance.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.TextField', [], {'max_length': '255'})
        },
        'assistance.questiontranslation': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'language'),)", 'object_name': 'QuestionTranslation'},
            'answer': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['assistance']
