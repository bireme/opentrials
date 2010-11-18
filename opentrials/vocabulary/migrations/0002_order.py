# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'StudyType.order'
        db.add_column('vocabulary_studytype', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)

        # Adding field 'AttachmentType.order'
        db.add_column('vocabulary_attachmenttype', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)

        # Adding field 'InterventionCode.order'
        db.add_column('vocabulary_interventioncode', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)

        # Adding field 'RecruitmentStatus.order'
        db.add_column('vocabulary_recruitmentstatus', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)

        # Adding field 'TrialNumberIssuingAuthority.order'
        db.add_column('vocabulary_trialnumberissuingauthority', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)

        # Adding field 'StudyPurpose.order'
        db.add_column('vocabulary_studypurpose', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)

        # Adding field 'CountryCode.order'
        db.add_column('vocabulary_countrycode', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)

        # Adding field 'StudyMasking.order'
        db.add_column('vocabulary_studymasking', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)

        # Adding field 'StudyAllocation.order'
        db.add_column('vocabulary_studyallocation', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)

        # Adding field 'StudyPhase.order'
        db.add_column('vocabulary_studyphase', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)

        # Adding field 'InterventionAssigment.order'
        db.add_column('vocabulary_interventionassigment', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)

        # Adding field 'IcdChapter.order'
        db.add_column('vocabulary_icdchapter', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)

        # Adding field 'DecsDisease.order'
        db.add_column('vocabulary_decsdisease', 'order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'StudyType.order'
        db.delete_column('vocabulary_studytype', 'order')

        # Deleting field 'AttachmentType.order'
        db.delete_column('vocabulary_attachmenttype', 'order')

        # Deleting field 'InterventionCode.order'
        db.delete_column('vocabulary_interventioncode', 'order')

        # Deleting field 'RecruitmentStatus.order'
        db.delete_column('vocabulary_recruitmentstatus', 'order')

        # Deleting field 'TrialNumberIssuingAuthority.order'
        db.delete_column('vocabulary_trialnumberissuingauthority', 'order')

        # Deleting field 'StudyPurpose.order'
        db.delete_column('vocabulary_studypurpose', 'order')

        # Deleting field 'CountryCode.order'
        db.delete_column('vocabulary_countrycode', 'order')

        # Deleting field 'StudyMasking.order'
        db.delete_column('vocabulary_studymasking', 'order')

        # Deleting field 'StudyAllocation.order'
        db.delete_column('vocabulary_studyallocation', 'order')

        # Deleting field 'StudyPhase.order'
        db.delete_column('vocabulary_studyphase', 'order')

        # Deleting field 'InterventionAssigment.order'
        db.delete_column('vocabulary_interventionassigment', 'order')

        # Deleting field 'IcdChapter.order'
        db.delete_column('vocabulary_icdchapter', 'order')

        # Deleting field 'DecsDisease.order'
        db.delete_column('vocabulary_decsdisease', 'order')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'vocabulary.attachmenttype': {
            'Meta': {'ordering': "['order']", 'object_name': 'AttachmentType'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'vocabulary.countrycode': {
            'Meta': {'ordering': "['description']", 'object_name': 'CountryCode'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'submission_language': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'vocabulary.decsdisease': {
            'Meta': {'ordering': "['order']", 'object_name': 'DecsDisease'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'vocabulary.icdchapter': {
            'Meta': {'ordering': "['order']", 'object_name': 'IcdChapter'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'vocabulary.interventionassigment': {
            'Meta': {'ordering': "['order']", 'object_name': 'InterventionAssigment'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'vocabulary.interventioncode': {
            'Meta': {'ordering': "['order']", 'object_name': 'InterventionCode'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'vocabulary.recruitmentstatus': {
            'Meta': {'object_name': 'RecruitmentStatus'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'vocabulary.studyallocation': {
            'Meta': {'ordering': "['order']", 'object_name': 'StudyAllocation'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'vocabulary.studymasking': {
            'Meta': {'ordering': "['order']", 'object_name': 'StudyMasking'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'vocabulary.studyphase': {
            'Meta': {'ordering': "['order']", 'object_name': 'StudyPhase'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'vocabulary.studypurpose': {
            'Meta': {'ordering': "['order']", 'object_name': 'StudyPurpose'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'vocabulary.studytype': {
            'Meta': {'ordering': "['order']", 'object_name': 'StudyType'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'vocabulary.trialnumberissuingauthority': {
            'Meta': {'object_name': 'TrialNumberIssuingAuthority'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
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
