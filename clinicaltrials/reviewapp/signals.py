def create_user_profile(sender, instance,**kwargs):
    from reviewapp.models import UserProfile
    UserProfile.objects.get_or_create(user=instance)

def check_trial_fields(sender, instance,**kwargs):
    
    REQUIRED_FIELDS = {
        'step_1': {
            'scientific_title': {'type': 'text', 'poly': True}
        }, 
        'step_2': {
            'primary_sponsor': {'type': 'text', 'poly': False}
        },
        'step_3': {
            'hc_freetext': {'type': 'text', 'poly': True}
        },
        'step_4': {
            'i_freetext': {'type': 'text', 'poly': True}, 
            'intervention_code': {'type': 'mult', 'poly': False, 'queryset': instance.intervention_code()}
        },
        'step_5': {
            'recruitment_status': {'type': 'text', 'poly': False}, 
            'recruitment_country': {'type': 'mult', 'poly': False, 'queryset': instance.recruitment_country.all()}, 
            'enrollment_start_planned': {'type': 'text', 'poly': False}, 
            'target_sample_size': {'type': 'text', 'poly': False}, 
            'inclusion_criteria': {'type': 'text', 'poly': True}, 
            'gender': {'type': 'text', 'poly': False}, 
            'agemin_value': {'type': 'text', 'poly': False}, 
            'agemin_unit': {'type': 'text', 'poly': False}, 
            'agemax_value': {'type': 'text', 'poly': False}, 
            'agemax_unit': {'type': 'text', 'poly': False}, 
            'exclusion_criteria': {'type': 'text', 'poly': True}
        },
        'step_6': {
            'study_type': {'type': 'text', 'poly': False}, 
            'study_design': {'type': 'text', 'poly': True}, 
            'phase': {'type': 'text', 'poly': False}
        },
        'step_7': {},
        'step_8': {}
    }
    
    OPTIONAL_FIELDS = {
        'step_1': {
            'scientific_acronym': {'type': 'text', 'poly': True},
            'scientific_acronym_expansion': {'type': 'text', 'poly': True},
            'public_title': {'type': 'text', 'poly': True},
            'acronym': {'type': 'text', 'poly': True},
            'acronym_expansion': {'type': 'text', 'poly': True}
        }, 
        'step_2': {},
        'step_3': {},
        'step_4': {},
        'step_5': {},
        'step_6': {
            'expanded_access_program': {'type': 'text', 'poly': False}, 
            'intervention_assignment': {'type': 'text', 'poly': False}, 
            'number_of_arms': {'type': 'text', 'poly': False},
            'masking': {'type': 'text', 'poly': False},
            'allocation': {'type': 'text', 'poly': False}
        },
        'step_7': {},
        'step_8': {}
    }
    
    from repository.trds_forms import STEP_FORM_MATRIX
    from repository.models import ClinicalTrial
    from settings import MANAGED_LANGUAGES
    import re
    import pickle

    fields_status = {'en': {'step_9': 'OK'}, 'es': {'step_9': 'OK'}, 'pt-br': {'step_9': 'OK'}}

    for step, forms in STEP_FORM_MATRIX.items():

        step_status = {}
        for form in forms:
            if hasattr(form.Meta,'queryset'):
                count = form.Meta.queryset.filter(trial=instance).count()
                
                if form.Meta.min_required != 0:
                    for lang in MANAGED_LANGUAGES:
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
                                            step_status.update({lang: 'MISSING'})
                                        elif type(value) is str or type(value) is unicode:
                                            if re.match('^\s*$', value):
                                                step_status.update({lang: 'MISSING'})
                                            else:
                                                if step_status.get(lang, '') == '':
                                                    step_status.update({lang: 'OK'})
                                        else:
                                            if len(str(value)) == 0:
                                                step_status.update({lang: 'MISSING'})
                                            else:
                                                if step_status.get(lang, '') == '':
                                                    step_status.update({lang: 'OK'})
                else:
                    for lang in MANAGED_LANGUAGES:
                        lang = lang.lower()
                        if count == 0:
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
                                            if step_status.get(lang, '') != 'MISSING':
                                                step_status.update({lang: 'BLANK'})
                                        elif type(value) is str or type(value) is unicode:
                                            if re.match('^\s*$', value):
                                                if step_status.get(lang, '') != 'MISSING':
                                                    step_status.update({lang: 'BLANK'})
                                            else:
                                                if step_status.get(lang, '') == '':
                                                    step_status.update({lang: 'OK'})
                                        else:
                                            if len(str(value)) == 0:
                                                if step_status.get(lang, '') != 'MISSING':
                                                    step_status.update({lang: 'BLANK'})
                                            else:
                                                if step_status.get(lang, '') == '':
                                                    step_status.update({lang: 'OK'})
                                    
            elif hasattr(form.Meta,'model'):
                if form.Meta.model == ClinicalTrial:
                    required_fields = REQUIRED_FIELDS[step]
                    optional_fields = OPTIONAL_FIELDS[step]
                    for field in form.declared_fields.keys():
                        values = {}
                        if field in required_fields.keys():
                            if required_fields[field]['type'] == 'text':
                                values.update({'en': getattr(instance, field)})
                                
                                for trans in instance.translations.all():
                                    if required_fields[field]['poly']:
                                        values.update({trans.language.lower(): getattr(trans, field)})
                                    else:
                                        values.update({trans.language.lower(): values['en']})
                                            
                                for lang, value in values.items():

                                    if value is None:
                                        step_status.update({lang: 'MISSING'})
                                    elif type(value) is str or type(value) is unicode:
                                        if re.match('^\s*$', value):
                                            step_status.update({lang: 'MISSING'})
                                        else:
                                            if step_status.get(lang, '') == '':
                                                step_status.update({lang: 'OK'})
                                    else:
                                        if len(str(value)) == 0:
                                            step_status.update({lang: 'MISSING'})
                                        else:
                                            if step_status.get(lang, '') == '':
                                                step_status.update({lang: 'OK'})
                                                    
                            elif required_fields[field]['type'] == 'mult':
                                count = required_fields[field]['queryset'].count()
                                if count < 1:
                                    for lang in MANAGED_LANGUAGES:
                                        lang = lang.lower()
                                        step_status.update({lang: 'MISSING'})
                                else:
                                    for lang in MANAGED_LANGUAGES:
                                        lang = lang.lower()
                                        if step_status.get(lang, '') == '':
                                            step_status.update({lang: 'OK'})
                            
                        elif field in optional_fields.keys():
                            if optional_fields[field]['type'] == 'text':
                                values.update({'en': getattr(instance, field)})

                                for trans in instance.translations.all():
                                    if optional_fields[field]['poly']:
                                        values.update({trans.language.lower(): getattr(trans, field)})
                                    else:
                                        values.update({trans.language.lower(): values['en']})
                                
                                for lang, value in values.items():
                                    if field == 'expanded_access_program':
                                        value = 'Ok' # because unknown value is None
                                        
                                    if value is None:
                                        if step_status.get(lang, '') != 'MISSING':
                                            step_status.update({lang: 'BLANK'})
                                    elif type(value) is str or type(value) is unicode:
                                        if re.match('^\s*$', value):
                                            if step_status.get(lang, '') != 'MISSING':
                                                step_status.update({lang: 'BLANK'})
                                        else:
                                            if step_status.get(lang, '') == '':
                                                step_status.update({lang: 'OK'})
                                    else:
                                        if len(str(value)) == 0:
                                            if step_status.get(lang, '') != 'MISSING':
                                                step_status.update({lang: 'BLANK'})
                                        else:
                                            if step_status.get(lang, '') == '':
                                                step_status.update({lang: 'OK'})
                      
        for language, status in step_status.items():
            if fields_status.get(language) is None:
                fields_status[language] = {step: status}
            else:
                fields_status[language].update({step: status})

    instance.submission.fields_status = pickle.dumps(fields_status)
    instance.submission.save()

