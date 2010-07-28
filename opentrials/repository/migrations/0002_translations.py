# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ClinicalTrialTranslation'
        db.create_table('repository_clinicaltrialtranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('scientific_title', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('scientific_acronym', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('scientific_acronym_expansion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('public_title', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('acronym_expansion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('hc_freetext', self.gf('django.db.models.fields.TextField')(max_length=8000, blank=True)),
            ('i_freetext', self.gf('django.db.models.fields.TextField')(max_length=8000, blank=True)),
            ('inclusion_criteria', self.gf('django.db.models.fields.TextField')(max_length=8000, blank=True)),
            ('exclusion_criteria', self.gf('django.db.models.fields.TextField')(max_length=8000, blank=True)),
            ('study_design', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
        ))
        db.send_create_signal('repository', ['ClinicalTrialTranslation'])

        # Adding model 'DescriptorTranslation'
        db.create_table('repository_descriptortranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('repository', ['DescriptorTranslation'])

        # Adding model 'OutcomeTranslation'
        db.create_table('repository_outcometranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=8000)),
        ))
        db.send_create_signal('repository', ['OutcomeTranslation'])


    def backwards(self, orm):
        
        # Deleting model 'ClinicalTrialTranslation'
        db.delete_table('repository_clinicaltrialtranslation')

        # Deleting model 'DescriptorTranslation'
        db.delete_table('repository_descriptortranslation')

        # Deleting model 'OutcomeTranslation'
        db.delete_table('repository_outcometranslation')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'repository.clinicaltrial': {
            'Meta': {'object_name': 'ClinicalTrial'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'acronym_expansion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'agemax_unit': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '1'}),
            'agemax_value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'agemin_unit': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '1'}),
            'agemin_value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'allocation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vocabulary.StudyAllocation']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_registration': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_index': 'True'}),
            'enrollment_end_actual': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'enrollment_end_planned': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'enrollment_start_actual': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'enrollment_start_planned': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'exclusion_criteria': ('django.db.models.fields.TextField', [], {'max_length': '8000', 'blank': 'True'}),
            'expanded_access_program': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'exported': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '1'}),
            'hc_freetext': ('django.db.models.fields.TextField', [], {'max_length': '8000', 'blank': 'True'}),
            'i_code': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['vocabulary.InterventionCode']", 'symmetrical': 'False'}),
            'i_freetext': ('django.db.models.fields.TextField', [], {'max_length': '8000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion_criteria': ('django.db.models.fields.TextField', [], {'max_length': '8000', 'blank': 'True'}),
            'intervention_assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vocabulary.InterventionAssigment']", 'null': 'True', 'blank': 'True'}),
            'masking': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vocabulary.StudyMasking']", 'null': 'True', 'blank': 'True'}),
            'number_of_arms': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vocabulary.StudyPhase']", 'null': 'True', 'blank': 'True'}),
            'primary_sponsor': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['repository.Institution']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'public_contact': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'public_contact_of_set'", 'symmetrical': 'False', 'through': "orm['repository.PublicContact']", 'to': "orm['repository.Contact']"}),
            'public_title': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'purpose': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vocabulary.StudyPurpose']", 'null': 'True', 'blank': 'True'}),
            'recruitment_country': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['vocabulary.CountryCode']", 'symmetrical': 'False'}),
            'recruitment_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vocabulary.RecruitmentStatus']", 'null': 'True', 'blank': 'True'}),
            'scientific_acronym': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'scientific_acronym_expansion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'scientific_contact': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'scientific_contact_of_set'", 'symmetrical': 'False', 'through': "orm['repository.ScientificContact']", 'to': "orm['repository.Contact']"}),
            'scientific_title': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'staff_note': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'processing'", 'max_length': '64'}),
            'study_design': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'study_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vocabulary.StudyType']", 'null': 'True', 'blank': 'True'}),
            'target_sample_size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'trial_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'repository.clinicaltrialtranslation': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'language'),)", 'object_name': 'ClinicalTrialTranslation'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'acronym_expansion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'exclusion_criteria': ('django.db.models.fields.TextField', [], {'max_length': '8000', 'blank': 'True'}),
            'hc_freetext': ('django.db.models.fields.TextField', [], {'max_length': '8000', 'blank': 'True'}),
            'i_freetext': ('django.db.models.fields.TextField', [], {'max_length': '8000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusion_criteria': ('django.db.models.fields.TextField', [], {'max_length': '8000', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'public_title': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'scientific_acronym': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'scientific_acronym_expansion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'scientific_title': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'study_design': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'})
        },
        'repository.contact': {
            'Meta': {'object_name': 'Contact'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Institution']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vocabulary.CountryCode']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'middlename': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'repository.descriptor': {
            'Meta': {'object_name': 'Descriptor'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'aspect': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.ClinicalTrial']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'vocabulary': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'repository.descriptortranslation': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'language'),)", 'object_name': 'DescriptorTranslation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'repository.institution': {
            'Meta': {'object_name': 'Institution'},
            'address': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vocabulary.CountryCode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'repository.outcome': {
            'Meta': {'object_name': 'Outcome'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '8000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.CharField', [], {'default': "'primary'", 'max_length': '32'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.ClinicalTrial']"})
        },
        'repository.outcometranslation': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'language'),)", 'object_name': 'OutcomeTranslation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '8000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'repository.publiccontact': {
            'Meta': {'unique_together': "(('trial', 'contact'),)", 'object_name': 'PublicContact'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Active'", 'max_length': '255'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.ClinicalTrial']"})
        },
        'repository.scientificcontact': {
            'Meta': {'unique_together': "(('trial', 'contact'),)", 'object_name': 'ScientificContact'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Active'", 'max_length': '255'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.ClinicalTrial']"})
        },
        'repository.sitecontact': {
            'Meta': {'unique_together': "(('trial', 'contact'),)", 'object_name': 'SiteContact'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Active'", 'max_length': '255'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.ClinicalTrial']"})
        },
        'repository.trialnumber': {
            'Meta': {'object_name': 'TrialNumber'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'issuing_authority': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.ClinicalTrial']"})
        },
        'repository.trialsecondarysponsor': {
            'Meta': {'object_name': 'TrialSecondarySponsor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Institution']"}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.ClinicalTrial']"})
        },
        'repository.trialsupportsource': {
            'Meta': {'object_name': 'TrialSupportSource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Institution']"}),
            'trial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.ClinicalTrial']"})
        },
        'vocabulary.countrycode': {
            'Meta': {'object_name': 'CountryCode'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'submission_language': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
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

    complete_apps = ['repository']
