# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ClinicalTrial'
        db.create_table('repository_clinicaltrial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trial_id', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True)),
            ('date_registration', self.gf('django.db.models.fields.DateField')(null=True, db_index=True)),
            ('scientific_title', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('scientific_acronym', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('scientific_acronym_expansion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('primary_sponsor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Institution'], null=True, blank=True)),
            ('public_title', self.gf('django.db.models.fields.TextField')(max_length=2000, blank=True)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('acronym_expansion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('hc_freetext', self.gf('django.db.models.fields.TextField')(max_length=8000, blank=True)),
            ('i_freetext', self.gf('django.db.models.fields.TextField')(max_length=8000, blank=True)),
            ('inclusion_criteria', self.gf('django.db.models.fields.TextField')(max_length=8000, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='-', max_length=1)),
            ('agemin_value', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
            ('agemin_unit', self.gf('django.db.models.fields.CharField')(default='-', max_length=1)),
            ('agemax_value', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
            ('agemax_unit', self.gf('django.db.models.fields.CharField')(default='-', max_length=1)),
            ('exclusion_criteria', self.gf('django.db.models.fields.TextField')(max_length=8000, blank=True)),
            ('study_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vocabulary.StudyType'], null=True, blank=True)),
            ('study_design', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
            ('expanded_access_program', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('purpose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vocabulary.StudyPurpose'], null=True, blank=True)),
            ('intervention_assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vocabulary.InterventionAssigment'], null=True, blank=True)),
            ('number_of_arms', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('masking', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vocabulary.StudyMasking'], null=True, blank=True)),
            ('allocation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vocabulary.StudyAllocation'], null=True, blank=True)),
            ('phase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vocabulary.StudyPhase'], null=True, blank=True)),
            ('enrollment_start_planned', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('enrollment_start_actual', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('enrollment_end_planned', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('enrollment_end_actual', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('target_sample_size', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('recruitment_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vocabulary.RecruitmentStatus'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('exported', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='processing', max_length=64)),
            ('staff_note', self.gf('django.db.models.fields.CharField')(max_length='255', blank=True)),
        ))
        db.send_create_signal('repository', ['ClinicalTrial'])

        # Adding M2M table for field i_code on 'ClinicalTrial'
        db.create_table('repository_clinicaltrial_i_code', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clinicaltrial', models.ForeignKey(orm['repository.clinicaltrial'], null=False)),
            ('interventioncode', models.ForeignKey(orm['vocabulary.interventioncode'], null=False))
        ))
        db.create_unique('repository_clinicaltrial_i_code', ['clinicaltrial_id', 'interventioncode_id'])

        # Adding M2M table for field recruitment_country on 'ClinicalTrial'
        db.create_table('repository_clinicaltrial_recruitment_country', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clinicaltrial', models.ForeignKey(orm['repository.clinicaltrial'], null=False)),
            ('countrycode', models.ForeignKey(orm['vocabulary.countrycode'], null=False))
        ))
        db.create_unique('repository_clinicaltrial_recruitment_country', ['clinicaltrial_id', 'countrycode_id'])

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

        # Adding unique constraint on 'ClinicalTrialTranslation', fields ['content_type', 'object_id', 'language']
        db.create_unique('repository_clinicaltrialtranslation', ['content_type_id', 'object_id', 'language'])

        # Adding model 'TrialNumber'
        db.create_table('repository_trialnumber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.ClinicalTrial'])),
            ('issuing_authority', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('id_number', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('repository', ['TrialNumber'])

        # Adding model 'TrialSecondarySponsor'
        db.create_table('repository_trialsecondarysponsor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.ClinicalTrial'])),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Institution'])),
        ))
        db.send_create_signal('repository', ['TrialSecondarySponsor'])

        # Adding model 'TrialSupportSource'
        db.create_table('repository_trialsupportsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.ClinicalTrial'])),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Institution'])),
        ))
        db.send_create_signal('repository', ['TrialSupportSource'])

        # Adding model 'Institution'
        db.create_table('repository_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.TextField')(max_length=1500, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vocabulary.CountryCode'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='institution_creator', to=orm['auth.User'])),
        ))
        db.send_create_signal('repository', ['Institution'])

        # Adding model 'Contact'
        db.create_table('repository_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('middlename', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('affiliation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Institution'], null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vocabulary.CountryCode'], null=True, blank=True)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contact_creator', to=orm['auth.User'])),
        ))
        db.send_create_signal('repository', ['Contact'])

        # Adding model 'PublicContact'
        db.create_table('repository_publiccontact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.ClinicalTrial'])),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Contact'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Active', max_length=255)),
        ))
        db.send_create_signal('repository', ['PublicContact'])

        # Adding unique constraint on 'PublicContact', fields ['trial', 'contact']
        db.create_unique('repository_publiccontact', ['trial_id', 'contact_id'])

        # Adding model 'ScientificContact'
        db.create_table('repository_scientificcontact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.ClinicalTrial'])),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Contact'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Active', max_length=255)),
        ))
        db.send_create_signal('repository', ['ScientificContact'])

        # Adding unique constraint on 'ScientificContact', fields ['trial', 'contact']
        db.create_unique('repository_scientificcontact', ['trial_id', 'contact_id'])

        # Adding model 'SiteContact'
        db.create_table('repository_sitecontact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.ClinicalTrial'])),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Contact'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Active', max_length=255)),
        ))
        db.send_create_signal('repository', ['SiteContact'])

        # Adding unique constraint on 'SiteContact', fields ['trial', 'contact']
        db.create_unique('repository_sitecontact', ['trial_id', 'contact_id'])

        # Adding model 'Outcome'
        db.create_table('repository_outcome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.ClinicalTrial'])),
            ('interest', self.gf('django.db.models.fields.CharField')(default='primary', max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=8000)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('repository', ['Outcome'])

        # Adding model 'OutcomeTranslation'
        db.create_table('repository_outcometranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=8000)),
        ))
        db.send_create_signal('repository', ['OutcomeTranslation'])

        # Adding unique constraint on 'OutcomeTranslation', fields ['content_type', 'object_id', 'language']
        db.create_unique('repository_outcometranslation', ['content_type_id', 'object_id', 'language'])

        # Adding model 'Descriptor'
        db.create_table('repository_descriptor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.ClinicalTrial'])),
            ('aspect', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('vocabulary', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('repository', ['Descriptor'])

        # Adding model 'DescriptorTranslation'
        db.create_table('repository_descriptortranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=8, db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('repository', ['DescriptorTranslation'])

        # Adding unique constraint on 'DescriptorTranslation', fields ['content_type', 'object_id', 'language']
        db.create_unique('repository_descriptortranslation', ['content_type_id', 'object_id', 'language'])


    def backwards(self, orm):
        
        # Deleting model 'ClinicalTrial'
        db.delete_table('repository_clinicaltrial')

        # Removing M2M table for field i_code on 'ClinicalTrial'
        db.delete_table('repository_clinicaltrial_i_code')

        # Removing M2M table for field recruitment_country on 'ClinicalTrial'
        db.delete_table('repository_clinicaltrial_recruitment_country')

        # Deleting model 'ClinicalTrialTranslation'
        db.delete_table('repository_clinicaltrialtranslation')

        # Removing unique constraint on 'ClinicalTrialTranslation', fields ['content_type', 'object_id', 'language']
        db.delete_unique('repository_clinicaltrialtranslation', ['content_type_id', 'object_id', 'language'])

        # Deleting model 'TrialNumber'
        db.delete_table('repository_trialnumber')

        # Deleting model 'TrialSecondarySponsor'
        db.delete_table('repository_trialsecondarysponsor')

        # Deleting model 'TrialSupportSource'
        db.delete_table('repository_trialsupportsource')

        # Deleting model 'Institution'
        db.delete_table('repository_institution')

        # Deleting model 'Contact'
        db.delete_table('repository_contact')

        # Deleting model 'PublicContact'
        db.delete_table('repository_publiccontact')

        # Removing unique constraint on 'PublicContact', fields ['trial', 'contact']
        db.delete_unique('repository_publiccontact', ['trial_id', 'contact_id'])

        # Deleting model 'ScientificContact'
        db.delete_table('repository_scientificcontact')

        # Removing unique constraint on 'ScientificContact', fields ['trial', 'contact']
        db.delete_unique('repository_scientificcontact', ['trial_id', 'contact_id'])

        # Deleting model 'SiteContact'
        db.delete_table('repository_sitecontact')

        # Removing unique constraint on 'SiteContact', fields ['trial', 'contact']
        db.delete_unique('repository_sitecontact', ['trial_id', 'contact_id'])

        # Deleting model 'Outcome'
        db.delete_table('repository_outcome')

        # Deleting model 'OutcomeTranslation'
        db.delete_table('repository_outcometranslation')

        # Removing unique constraint on 'OutcomeTranslation', fields ['content_type', 'object_id', 'language']
        db.delete_unique('repository_outcometranslation', ['content_type_id', 'object_id', 'language'])

        # Deleting model 'Descriptor'
        db.delete_table('repository_descriptor')

        # Deleting model 'DescriptorTranslation'
        db.delete_table('repository_descriptortranslation')

        # Removing unique constraint on 'DescriptorTranslation', fields ['content_type', 'object_id', 'language']
        db.delete_unique('repository_descriptortranslation', ['content_type_id', 'object_id', 'language'])


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
        'repository.clinicaltrial': {
            'Meta': {'object_name': 'ClinicalTrial'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'acronym_expansion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'agemax_unit': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '1'}),
            'agemax_value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'agemin_unit': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '1'}),
            'agemin_value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'allocation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vocabulary.StudyAllocation']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_registration': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_index': 'True'}),
            'enrollment_end_actual': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'enrollment_end_planned': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'enrollment_start_actual': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'enrollment_start_planned': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
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
            'primary_sponsor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Institution']", 'null': 'True', 'blank': 'True'}),
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
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contact_creator'", 'to': "orm['auth.User']"}),
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
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'institution_creator'", 'to': "orm['auth.User']"}),
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
