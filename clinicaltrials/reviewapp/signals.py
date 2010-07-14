def create_user_profile(sender, instance,**kwargs):
    from reviewapp.models import UserProfile
    UserProfile.objects.get_or_create(user=instance)

def check_trial_fields(sender, instance,**kwargs):

    if not hasattr(instance, 'submission'):
        return
    
    FIELDS = {
        'step_1': {
            'scientific_title': {'required': True, 'type': 'text', 'poly': True},
            'scientific_acronym': {'required': False, 'type': 'text', 'poly': True},
            'scientific_acronym_expansion': {'required': False, 'type': 'text', 'poly': True},
            'public_title': {'required': False, 'type': 'text', 'poly': True},
            'acronym': {'required': False, 'type': 'text', 'poly': True},
            'acronym_expansion': {'required': False, 'type': 'text', 'poly': True}
        }, 
        'step_2': {
            'primary_sponsor': {'required': True, 'type': 'text', 'poly': False}
        },
        'step_3': {
            'hc_freetext': {'required': True, 'type': 'text', 'poly': True}
        },
        'step_4': {
            'i_freetext': {'required': True, 'type': 'text', 'poly': True}, 
            'intervention_code': {'required': True, 'type': 'mult', 'poly': False, 
                                  'queryset': instance.intervention_code()}
        },
        'step_5': {
            'recruitment_status': {'required': True, 'type': 'text', 'poly': False}, 
            'recruitment_country': {'required': True, 'type': 'mult', 'poly': False, 
                                    'queryset': instance.recruitment_country.all()}, 
            'enrollment_start_planned': {'required': True, 'type': 'text', 'poly': False}, 
            'target_sample_size': {'required': True, 'type': 'text', 'poly': False}, 
            'inclusion_criteria': {'required': True, 'type': 'text', 'poly': True}, 
            'gender': {'required': True, 'type': 'text', 'poly': False}, 
            'agemin_value': {'required': True, 'type': 'text', 'poly': False}, 
            'agemin_unit': {'required': True, 'type': 'text', 'poly': False}, 
            'agemax_value': {'required': True, 'type': 'text', 'poly': False}, 
            'agemax_unit': {'required': True, 'type': 'text', 'poly': False}, 
        },
        'step_6': {
            'study_type': {'required': True, 'type': 'text', 'poly': False}, 
            'study_design': {'required': True, 'type': 'text', 'poly': True}, 
            'phase': {'required': True, 'type': 'text', 'poly': False},
            #'expanded_access_program': {'required': False, 'type': 'text', 'poly': False}, 
            'intervention_assignment': {'required': False, 'type': 'text', 'poly': False}, 
            'number_of_arms': {'required': False, 'type': 'text', 'poly': False},
            'masking': {'required': False, 'type': 'text', 'poly': False},
            'allocation': {'required': False, 'type': 'text', 'poly': False}
        },
        'step_7': {},
        'step_8': {}
    }
    
    from repository.trds_forms import STEP_FORM_MATRIX
    from repository.models import ClinicalTrial
    import re
    import pickle

    fields_status = {}

    # attachment
    count = instance.submission.attachment_set.all().count()
    for lang in instance.submission.get_mandatory_languages():
        lang = lang.lower()
        if count == 0:
            fields_status.update({lang: {'step_9': 'BLANK'}})
        else:
            fields_status.update({lang: {'step_9': 'OK'}})

    for step, forms in STEP_FORM_MATRIX.items():

        step_status = {}
        for form in forms:
            if hasattr(form.Meta,'queryset'):
                count = form.Meta.queryset.filter(trial=instance).count()
                
                for lang in instance.submission.get_mandatory_languages():
                    lang = lang.lower()
                    if count < form.Meta.min_required:
                        step_status.update({lang: 'MISSING'})
                    elif count == 0:
                        if step_status.get(lang, '') != 'MISSING':
                            step_status.update({lang: 'BLANK'})
                    else:
                        if not form.Meta.polyglot:
                            if step_status.get(lang, '') == '':
                                step_status.update({lang: 'OK'})
                        else:
                            for out in form.Meta.queryset.filter(trial=instance):
                                for field in form.Meta.polyglot_fields:
                                    if lang == 'en':
                                        value = [getattr(out, field)]
                                    else:
                                        list_value = out.translations.filter(language=lang)
                                        if len(list_value) > 0:
                                            value = getattr(list_value[0], field)
                                        else:
                                            value = None

                                    if value is None:
                                        if form.Meta.min_required != 0:
                                            step_status.update({lang: 'MISSING'})
                                        else:
                                            if step_status.get(lang, '') != 'MISSING':
                                                step_status.update({lang: 'BLANK'})
                                    elif type(value) is str or type(value) is unicode:
                                        if re.match('^\s*$', value):
                                            if step_status.get(lang, '') != 'MISSING':
                                                step_status.update({lang: 'MISSING'})
                                            else:
                                                if step_status.get(lang, '') != 'MISSING':
                                                    step_status.update({lang: 'BLANK'})
                                        else:
                                            if step_status.get(lang, '') == '':
                                                step_status.update({lang: 'OK'})
                                    else:
                                        if len(str(value)) == 0:
                                            if form.Meta.min_required != 0:
                                                step_status.update({lang: 'MISSING'})
                                            else:
                                                if step_status.get(lang, '') != 'MISSING':
                                                    step_status.update({lang: 'BLANK'})
                                        else:
                                            if step_status.get(lang, '') == '':
                                                step_status.update({lang: 'OK'})
            
            else:
                if hasattr(form.Meta,'model'):
                    if form.Meta.model == ClinicalTrial:
                        check_fields = FIELDS[step]
                        for field in form.declared_fields.keys():
                            values = {}
                            if field in check_fields.keys():
                                if check_fields[field]['type'] == 'text':
                                    values.update({'en': getattr(instance, field)})
                                    
                                    for trans in instance.translations.all():
                                        if check_fields[field]['poly']:
                                            values.update({trans.language.lower(): getattr(trans, field)})
                                        else:
                                            values.update({trans.language.lower(): values['en']})
                                                
                                    for lang, value in values.items():
                                        if value is None:
                                            if check_fields[field]['required']:
                                                step_status.update({lang: 'MISSING'})
                                            else:
                                                if step_status.get(lang, '') != 'MISSING':
                                                    step_status.update({lang: 'BLANK'})
                                        elif type(value) is str or type(value) is unicode:
                                            if re.match('^\s*$', value):
                                                if check_fields[field]['required']:
                                                    step_status.update({lang: 'MISSING'})
                                                else:
                                                    if step_status.get(lang, '') != 'MISSING':
                                                        step_status.update({lang: 'BLANK'})
                                            else:
                                                if step_status.get(lang, '') == '':
                                                    step_status.update({lang: 'OK'})
                                        else:
                                            if len(str(value)) == 0:
                                                if check_fields[field]['required']:
                                                    step_status.update({lang: 'MISSING'})
                                                else:
                                                    if step_status.get(lang, '') != 'MISSING':
                                                        step_status.update({lang: 'BLANK'})
                                            else:
                                                if step_status.get(lang, '') == '':
                                                    step_status.update({lang: 'OK'})
                                
                                else: 
                                    if check_fields[field]['type'] == 'mult':
                                        count = check_fields[field]['queryset'].count()

                                        for lang in instance.submission.get_mandatory_languages():
                                            lang = lang.lower()
                                            if count < 1:
                                                step_status.update({lang: 'MISSING'})
                                            else:
                                                if step_status.get(lang, '') == '':
                                                    step_status.update({lang: 'OK'})
                                

        for language, status in step_status.items():
            if fields_status.get(language) is None:
                fields_status[language] = {step: status}
            else:
                fields_status[language].update({step: status})

    # TODO: the next two lines generate an exception on syncdb,
    # we need to find a work around for this, perhaps detecting
    # when the signal is not fired by user action but by a
    # bulk data load.
    # Remove try/except (fix and revise code)

    instance.submission.fields_status = pickle.dumps(fields_status)
    instance.submission.save()

    # The exception:
    #Installing json fixture 'initial_data' from '/home/luciano/prj/ct/svn/trunk/clinicaltrials/repository/fixtures'.
    #Problem installing fixture '/home/luciano/prj/ct/svn/trunk/clinicaltrials/repository/fixtures/initial_data.json': Traceback (most recent call last):
      #File "/home/luciano/prj/ct/django1.2-env/lib/python2.6/site-packages/Django-1.2.1-py2.6.egg/django/core/management/commands/loaddata.py", line 169, in handle
        #obj.save(using=using)
      #File "/home/luciano/prj/ct/django1.2-env/lib/python2.6/site-packages/Django-1.2.1-py2.6.egg/django/core/serializers/base.py", line 165, in save
        #models.Model.save_base(self.object, using=using, raw=True)
      #File "/home/luciano/prj/ct/django1.2-env/lib/python2.6/site-packages/Django-1.2.1-py2.6.egg/django/db/models/base.py", line 543, in save_base
        #created=(not record_exists), raw=raw)
      #File "/home/luciano/prj/ct/django1.2-env/lib/python2.6/site-packages/Django-1.2.1-py2.6.egg/django/dispatch/dispatcher.py", line 162, in send
        #response = receiver(signal=self, sender=sender, **named)
      #File "/home/luciano/prj/ct/svn/trunk/clinicaltrials/reviewapp/signals.py", line 242, in check_trial_fields
        #instance.submission.fields_status = pickle.dumps(fields_status)
      #File "/home/luciano/prj/ct/django1.2-env/lib/python2.6/site-packages/Django-1.2.1-py2.6.egg/django/db/models/fields/related.py", line 226, in __get__
        #rel_obj = self.related.model._base_manager.using(db).get(**params)
      #File "/home/luciano/prj/ct/django1.2-env/lib/python2.6/site-packages/Django-1.2.1-py2.6.egg/django/db/models/query.py", line 341, in get
        #% self.model._meta.object_name)
    #DoesNotExist: Submission matching query does not exist.

