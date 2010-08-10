"""
This module aims to be the refactored code of old function "reviewapp/signals.py:check_trial_fields"

The method trial_validator.register() was created in replacement to STEP_FORM_MATRIX
"""

import re, pickle # XXX: simplejson is more elegant than pickle to serialize validation messages

from django.template.defaultfilters import slugify

from reviewapp.consts import STEP_STATES, REMARK, MISSING, PARTIAL, COMPLETE, TRIAL_FORMS
from polyglot.multilingual_forms import BaseMultilingualWidget

FIELDS = {
    TRIAL_FORMS[0]: {
        'scientific_title': {'required': True, 'type': 'text', 'poly': True},
        'scientific_acronym': {'required': False, 'type': 'text', 'poly': True},
        'scientific_acronym_expansion': {'required': False, 'type': 'text', 'poly': True},
        'public_title': {'required': False, 'type': 'text', 'poly': True},
        'acronym': {'required': False, 'type': 'text', 'poly': True},
        'acronym_expansion': {'required': False, 'type': 'text', 'poly': True}
    }, 
    TRIAL_FORMS[1]: {
        'primary_sponsor': {'required': True, 'type': 'text', 'poly': False}
    },
    TRIAL_FORMS[2]: {
        'hc_freetext': {'required': True, 'type': 'text', 'poly': True}
    },
    TRIAL_FORMS[3]: {
        'i_freetext': {'required': True, 'type': 'text', 'poly': True}, 
        'i_code': {'required': True, 'type': 'mult', 'poly': False, 'queryset': None}
    },
    TRIAL_FORMS[4]: {
        'recruitment_status': {'required': True, 'type': 'text', 'poly': False}, 
        'recruitment_country': {'required': True, 'type': 'mult', 'poly': False, 'queryset': None},
        'enrollment_start_planned': {'required': True, 'type': 'text', 'poly': False},
        #'enrollment_end_planned': {'required': True, 'type': 'text', 'poly': False},  
        'target_sample_size': {'required': True, 'type': 'text', 'poly': False}, 
        'inclusion_criteria': {'required': True, 'type': 'text', 'poly': True},
        'exclusion_criteria': {'required': True, 'type': 'text', 'poly': True},  
        'gender': {'required': True, 'type': 'text', 'poly': False}, 
        'agemin_value': {'required': True, 'type': 'text', 'poly': False}, 
        'agemin_unit': {'required': True, 'type': 'text', 'poly': False}, 
        'agemax_value': {'required': True, 'type': 'text', 'poly': False}, 
        'agemax_unit': {'required': True, 'type': 'text', 'poly': False}, 
    },
    TRIAL_FORMS[5]: {
        #'study_type': {'required': True, 'type': 'text', 'poly': False}, 
        'study_design': {'required': True, 'type': 'text', 'poly': True}, 
        'phase': {'required': True, 'type': 'text', 'poly': False},
        'expanded_access_program': {'required': True, 'type': 'text', 'poly': False}, 
        'intervention_assignment': {'required': True, 'type': 'text', 'poly': False}, 
        'number_of_arms': {'required': True, 'type': 'text', 'poly': False},
        'masking': {'required': True, 'type': 'text', 'poly': False},
        'allocation': {'required': True, 'type': 'text', 'poly': False},
        'purpose': {'required': True, 'type': 'text', 'poly': False}
    },
    TRIAL_FORMS[6]: {},
    TRIAL_FORMS[7]: {}
}

class TrialValidator(object):
    steps_forms = None # Replaced STEP_FORM_MATRIX
    model = None
    
    def __init__(self):
        self.steps_forms = {}

    def register(self, step, forms):
        self.steps_forms[step] = forms

    def validate(self, instance):
        """
        FIXME: Some thoughts about this function:

        - Should have comments/docs/tests
        - Should be refactored (in progress)
        - Seems to be too complex for what it does
        """

        if not hasattr(instance, 'submission'):
            return
        
        fields_status = {}

        # Setting instance queryset on validation fields
        FIELDS[TRIAL_FORMS[3]]['i_code']['queryset'] = instance.intervention_code()
        FIELDS[TRIAL_FORMS[4]]['recruitment_country']['queryset'] = instance.recruitment_country.all()

        # attachment
        remarks = instance.submission.remark_set.filter(status='opened').filter(context=slugify(TRIAL_FORMS[8])).count()
        count = instance.submission.attachment_set.all().count()
        for lang in instance.submission.get_mandatory_languages():
            lang = lang.lower()
            if remarks > 0:
                fields_status.update({lang: {TRIAL_FORMS[8]: REMARK}})
            elif count == 0:
                fields_status.update({lang: {TRIAL_FORMS[8]: PARTIAL}})
            else:
                fields_status.update({lang: {TRIAL_FORMS[8]: COMPLETE}})

        for step, forms in self.steps_forms.items():
        
            step_status = {}
            
            remarks = instance.submission.remark_set.filter(status='opened').filter(context=slugify(step)).count()
            if remarks > 0:
                for lang in instance.submission.get_mandatory_languages():
                    lang = lang.lower()
                    step_status.update({lang: REMARK})
            else:
                for form in forms:
                    if hasattr(form.Meta,'queryset'):
                        count = form.Meta.queryset.filter(trial=instance).count()
                        
                        for lang in instance.submission.get_mandatory_languages():
                            lang = lang.lower()
                            if count < form.Meta.min_required:
                                step_status.update({lang: MISSING})
                            elif count == 0:
                                if step_status.get(lang, '') != MISSING:
                                    step_status.update({lang: PARTIAL})
                            else:
                                if not form.Meta.polyglot:
                                    if step_status.get(lang, '') == '':
                                        step_status.update({lang: COMPLETE})
                                else:
                                    for obj in form.Meta.queryset.filter(trial=instance):
                                        for field in form.Meta.polyglot_fields:
                                            if lang == 'en':
                                                value = [getattr(obj, field)]
                                            else:
                                                list_value = obj.translations.filter(language=lang)
                                                if len(list_value) > 0:
                                                    value = getattr(list_value[0], field)
                                                else:
                                                    value = None

                                            if value is None:
                                                if form.Meta.min_required != 0:
                                                    step_status.update({lang: MISSING})
                                                else:
                                                    if step_status.get(lang, '') != MISSING:
                                                        step_status.update({lang: PARTIAL})
                                            elif type(value) is str or type(value) is unicode:
                                                if re.match('^\s*$', value):
                                                    if step_status.get(lang, '') != MISSING:
                                                        step_status.update({lang: MISSING})
                                                    else:
                                                        if step_status.get(lang, '') != MISSING:
                                                            step_status.update({lang: PARTIAL})
                                                else:
                                                    if step_status.get(lang, '') == '':
                                                        step_status.update({lang: COMPLETE})
                                            else:
                                                if len(str(value)) == 0:
                                                    if form.Meta.min_required != 0:
                                                        step_status.update({lang: MISSING})
                                                    else:
                                                        if step_status.get(lang, '') != MISSING:
                                                            step_status.update({lang: PARTIAL})
                                                else:
                                                    if step_status.get(lang, '') == '':
                                                        step_status.update({lang: COMPLETE})
                    
                    else:
                        if hasattr(form.Meta,'model'):
                            if form.Meta.model == self.model:
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
                                                        step_status.update({lang: MISSING})
                                                    else:
                                                        if step_status.get(lang, '') != MISSING:
                                                            step_status.update({lang: PARTIAL})
                                                elif type(value) is str or type(value) is unicode:
                                                    if re.match('^\s*$', value):
                                                        if check_fields[field]['required']:
                                                            step_status.update({lang: MISSING})
                                                        else:
                                                            if step_status.get(lang, '') != MISSING:
                                                                step_status.update({lang: PARTIAL})
                                                    else:
                                                        if step_status.get(lang, '') == '':
                                                            step_status.update({lang: COMPLETE})
                                                else:
                                                    if len(str(value)) == 0:
                                                        if check_fields[field]['required']:
                                                            step_status.update({lang: MISSING})
                                                        else:
                                                            if step_status.get(lang, '') != MISSING:
                                                                step_status.update({lang: PARTIAL})
                                                    else:
                                                        if step_status.get(lang, '') == '':
                                                            step_status.update({lang: COMPLETE})
                                        
                                        else: 
                                            if check_fields[field]['type'] == 'mult':
                                                count = check_fields[field]['queryset'].count()

                                                for lang in instance.submission.get_mandatory_languages():
                                                    lang = lang.lower()
                                                    if count < 1:
                                                        step_status.update({lang: MISSING})
                                                    else:
                                                        if step_status.get(lang, '') == '':
                                                            step_status.update({lang: COMPLETE})

            for language, status in step_status.items():
                if fields_status.get(language) is None:
                    fields_status[language] = {step: status}
                else:
                    fields_status[language].update({step: status})


        # Stores the serialized dictionary with fields statuses in the submission, to be
        # used in further later, when showing the form (also to block before the trial go
        # to the next state)
        instance.submission.fields_status = pickle.dumps(fields_status)
        instance.submission.save()

    def field_is_required(self, form, field_name):
        """Returns a boolean value about this is a required field according to validation rules"""

        # Returns this is or is not a required field
        try:
            rules = self.get_rules_by_field(form, field_name)

            if rules:
                return rules['required']
        except KeyError:
            pass
    
    def get_rules_by_field(self, form, field_name):
        """Returns a dictionary with rules from constant FIELDS for a given field."""

        # Gets step where the given form is
        step_in = None
        for step, forms in self.steps_forms.items():
            if form.__class__ in forms:
                step_in = step
                break

        # Returns the rules from a dictionary
        try:
            return FIELDS[step_in][field_name]
        except KeyError:
            pass

    def get_field_status(self, form, field_name, instance):
        """Returns the status of a given field, for a given instance.submission"""

        rules = self.get_rules_by_field(form, field_name)

        if rules and rules['required']:
            if field_name in form.fields:
                field = form.fields[field_name]
                field_value = form.initial.get(field_name, None)

                # For multilingual fields
                if isinstance(field.widget, BaseMultilingualWidget):
                    # Default language value (english)
                    values = [field_value]

                    # Values for available languages (except to english)
                    for lang in field.available_languages:
                        if lang != 'en':
                            values.append(field.widget.get_value_by_language(field_name, field_value, lang))

                    # Returns "required" if any of translation values is not valid
                    if not all(values):
                        return 'required'

                # For common fields
                elif not field_value:
                    return 'required'

        return ''

trial_validator = TrialValidator()

