# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('assistance_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('assistance', ['Category'])

        # Adding model 'CategoryTranslation'
        db.create_table('assistance_categorytranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('assistance', ['CategoryTranslation'])

        # Adding unique constraint on 'CategoryTranslation', fields ['content_type', 'object_id', 'language']
        db.create_unique('assistance_categorytranslation', ['content_type_id', 'object_id', 'language'])

        # Adding model 'Question'
        db.create_table('assistance_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assistance.Category'])),
            ('title', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('answer', self.gf('django.db.models.fields.TextField')(max_length=2048)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('assistance', ['Question'])

        # Adding model 'QuestionTranslation'
        db.create_table('assistance_questiontranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('title', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('answer', self.gf('django.db.models.fields.TextField')(max_length=2048)),
        ))
        db.send_create_signal('assistance', ['QuestionTranslation'])

        # Adding unique constraint on 'QuestionTranslation', fields ['content_type', 'object_id', 'language']
        db.create_unique('assistance_questiontranslation', ['content_type_id', 'object_id', 'language'])

        # Adding model 'FieldHelp'
        db.create_table('assistance_fieldhelp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('form', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=2048, blank=True)),
            ('example', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('assistance', ['FieldHelp'])

        # Adding unique constraint on 'FieldHelp', fields ['form', 'field']
        db.create_unique('assistance_fieldhelp', ['form', 'field'])

        # Adding model 'FieldHelpTranslation'
        db.create_table('assistance_fieldhelptranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=2048, blank=True)),
            ('example', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('assistance', ['FieldHelpTranslation'])

        # Adding unique constraint on 'FieldHelpTranslation', fields ['content_type', 'object_id', 'language']
        db.create_unique('assistance_fieldhelptranslation', ['content_type_id', 'object_id', 'language'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('assistance_category')

        # Deleting model 'CategoryTranslation'
        db.delete_table('assistance_categorytranslation')

        # Removing unique constraint on 'CategoryTranslation', fields ['content_type', 'object_id', 'language']
        db.delete_unique('assistance_categorytranslation', ['content_type_id', 'object_id', 'language'])

        # Deleting model 'Question'
        db.delete_table('assistance_question')

        # Deleting model 'QuestionTranslation'
        db.delete_table('assistance_questiontranslation')

        # Removing unique constraint on 'QuestionTranslation', fields ['content_type', 'object_id', 'language']
        db.delete_unique('assistance_questiontranslation', ['content_type_id', 'object_id', 'language'])

        # Deleting model 'FieldHelp'
        db.delete_table('assistance_fieldhelp')

        # Removing unique constraint on 'FieldHelp', fields ['form', 'field']
        db.delete_unique('assistance_fieldhelp', ['form', 'field'])

        # Deleting model 'FieldHelpTranslation'
        db.delete_table('assistance_fieldhelptranslation')

        # Removing unique constraint on 'FieldHelpTranslation', fields ['content_type', 'object_id', 'language']
        db.delete_unique('assistance_fieldhelptranslation', ['content_type_id', 'object_id', 'language'])


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
            'Meta': {'unique_together': "(('form', 'field'),)", 'object_name': 'FieldHelp'},
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
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['assistance']
