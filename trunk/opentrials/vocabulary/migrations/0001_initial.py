# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'VocabularyTranslation'
        db.create_table('vocabulary_vocabularytranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['VocabularyTranslation'])

        # Adding unique constraint on 'VocabularyTranslation', fields ['content_type', 'object_id', 'language']
        db.create_unique('vocabulary_vocabularytranslation', ['content_type_id', 'object_id', 'language'])

        # Adding model 'CountryCode'
        db.create_table('vocabulary_countrycode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
            ('submission_language', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['CountryCode'])

        # Adding model 'TrialNumberIssuingAuthority'
        db.create_table('vocabulary_trialnumberissuingauthority', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['TrialNumberIssuingAuthority'])

        # Adding model 'InterventionCode'
        db.create_table('vocabulary_interventioncode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['InterventionCode'])

        # Adding model 'StudyType'
        db.create_table('vocabulary_studytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['StudyType'])

        # Adding model 'StudyPurpose'
        db.create_table('vocabulary_studypurpose', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['StudyPurpose'])

        # Adding model 'InterventionAssigment'
        db.create_table('vocabulary_interventionassigment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['InterventionAssigment'])

        # Adding model 'StudyMasking'
        db.create_table('vocabulary_studymasking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['StudyMasking'])

        # Adding model 'StudyAllocation'
        db.create_table('vocabulary_studyallocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['StudyAllocation'])

        # Adding model 'StudyPhase'
        db.create_table('vocabulary_studyphase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['StudyPhase'])

        # Adding model 'RecruitmentStatus'
        db.create_table('vocabulary_recruitmentstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['RecruitmentStatus'])

        # Adding model 'DecsDisease'
        db.create_table('vocabulary_decsdisease', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['DecsDisease'])

        # Adding model 'IcdChapter'
        db.create_table('vocabulary_icdchapter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['IcdChapter'])

        # Adding model 'AttachmentType'
        db.create_table('vocabulary_attachmenttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('vocabulary', ['AttachmentType'])


    def backwards(self, orm):
        
        # Deleting model 'VocabularyTranslation'
        db.delete_table('vocabulary_vocabularytranslation')

        # Removing unique constraint on 'VocabularyTranslation', fields ['content_type', 'object_id', 'language']
        db.delete_unique('vocabulary_vocabularytranslation', ['content_type_id', 'object_id', 'language'])

        # Deleting model 'CountryCode'
        db.delete_table('vocabulary_countrycode')

        # Deleting model 'TrialNumberIssuingAuthority'
        db.delete_table('vocabulary_trialnumberissuingauthority')

        # Deleting model 'InterventionCode'
        db.delete_table('vocabulary_interventioncode')

        # Deleting model 'StudyType'
        db.delete_table('vocabulary_studytype')

        # Deleting model 'StudyPurpose'
        db.delete_table('vocabulary_studypurpose')

        # Deleting model 'InterventionAssigment'
        db.delete_table('vocabulary_interventionassigment')

        # Deleting model 'StudyMasking'
        db.delete_table('vocabulary_studymasking')

        # Deleting model 'StudyAllocation'
        db.delete_table('vocabulary_studyallocation')

        # Deleting model 'StudyPhase'
        db.delete_table('vocabulary_studyphase')

        # Deleting model 'RecruitmentStatus'
        db.delete_table('vocabulary_recruitmentstatus')

        # Deleting model 'DecsDisease'
        db.delete_table('vocabulary_decsdisease')

        # Deleting model 'IcdChapter'
        db.delete_table('vocabulary_icdchapter')

        # Deleting model 'AttachmentType'
        db.delete_table('vocabulary_attachmenttype')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'vocabulary.attachmenttype': {
            'Meta': {'object_name': 'AttachmentType'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vocabulary.countrycode': {
            'Meta': {'object_name': 'CountryCode'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'submission_language': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'vocabulary.decsdisease': {
            'Meta': {'object_name': 'DecsDisease'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vocabulary.icdchapter': {
            'Meta': {'object_name': 'IcdChapter'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vocabulary.interventionassigment': {
            'Meta': {'object_name': 'InterventionAssigment'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vocabulary.interventioncode': {
            'Meta': {'object_name': 'InterventionCode'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vocabulary.recruitmentstatus': {
            'Meta': {'object_name': 'RecruitmentStatus'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vocabulary.studyallocation': {
            'Meta': {'object_name': 'StudyAllocation'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vocabulary.studymasking': {
            'Meta': {'object_name': 'StudyMasking'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vocabulary.studyphase': {
            'Meta': {'object_name': 'StudyPhase'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vocabulary.studypurpose': {
            'Meta': {'object_name': 'StudyPurpose'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vocabulary.studytype': {
            'Meta': {'object_name': 'StudyType'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vocabulary.trialnumberissuingauthority': {
            'Meta': {'object_name': 'TrialNumberIssuingAuthority'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'vocabulary.vocabularytranslation': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'language'),)", 'object_name': 'VocabularyTranslation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['vocabulary']
