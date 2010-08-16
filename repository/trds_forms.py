#coding: utf-8

from assistance.models import FieldHelp
from vocabulary.models import CountryCode
from repository.models import ClinicalTrial, Contact, Descriptor, Institution
from repository.models import InterventionCode, Outcome, RecruitmentStatus
from repository.models import StudyPhase, TrialSecondarySponsor, TrialSupportSource
from repository.models import SiteContact, PublicContact, ScientificContact
from repository.models import TrialNumber

import choices

from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.forms.formsets import DELETION_FIELD_NAME
from django.template.defaultfilters import linebreaksbr

from django import forms
from django.forms.forms import BoundField, conditional_escape

from polyglot.multilingual_forms import MultilingualCharField, MultilingualTextField
from polyglot.multilingual_forms import MultilingualModelChoiceField, MultilingualModelMultipleChoiceField
from polyglot.multilingual_forms import MultilingualBaseForm, MultilingualBaseFormSet

from trial_validation import trial_validator, TRIAL_FORMS

from datetime import date

import settings

class ReviewModelForm(MultilingualBaseForm):

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."

        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        output, hidden_fields = [], []
        for name, field in self.fields.items():
            bf = BoundField(self, field, name)
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_unicode(bf_errors))
                if bf.label:
                    label = conditional_escape(force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if self.label_suffix:
                        if label[-1] not in ':?.!':
                            label += self.label_suffix
                    # Sets label with an asterisk if this is a obligatory field according to to validation rules
                    if trial_validator.field_is_required(self, name):
                        label = '* ' + label
                    label = bf.label_tag(label) or ''
                else:
                    label = ''


                # Gets the field status for this field to use it as CSS class
                if self.instance:
                    field_status = trial_validator.get_field_status(self, name, self.instance)
                else:
                    field_status = ''

                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = u''
                form_name = self.__class__.__name__
                #import pdb; pdb.set_trace()
                help_record, new = FieldHelp.objects.get_or_create(form=form_name, field=name)
                help_text = help_text + u' ' + force_unicode(help_record)
                help_text = linebreaksbr(help_text_html % help_text)
                output.append(normal_row % {'errors': force_unicode(bf_errors),
                                            'label': force_unicode(label),
                                            'field': unicode(bf),
                                            'help_text': help_text,
                                            'help_id': 'id_%s-help%s' % ((self.prefix or name),help_record.pk),
                                            'field_class': field_status,
                                            })
        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))
        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)

            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = normal_row % {'errors': '',
                                             'label': '',
                                             'field': '',
                                             'help_text': '',
                                             'help_id': 'id_%s-help%s' % (self.prefix,help_record.pk),
                                             'issue': '',}
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)

        return mark_safe(u'\n'.join(output))

    def as_table(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        normal_row = u'''
            <tr class="%(field_class)s"><th><img src="/static/help.png" rel="#%(help_id)s"/>
                    <div id="%(help_id)s" class="help">%(help_text)s</div>
                    %(label)s</th>
                <td>%(errors)s%(field)s
                </td></tr>'''
        return self._html_output(normal_row=normal_row,
                                 error_row=u'<tr><td colspan="3">%s</td></tr>',
                                 row_ender='</td></tr>',
                                 help_text_html=u'%s',
                                 errors_on_separate_row=False)

#
# Forms
#


### step_1 #####################################################################
class TrialIdentificationForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['scientific_title','scientific_acronym',
                  'scientific_acronym_expansion',
                  'public_title','acronym','acronym_expansion']

    title = _('Trial Identification')
    # TRDS 10a
    scientific_title = forms.CharField(label=_('Scientific Title'),
                                       max_length=2000,
                                       widget=forms.Textarea)
    # TRDS 10b
    scientific_acronym = forms.CharField(required=False,
                                         label=_('Scientific Acronym'),
                                         max_length=255)
    # TRDS 9a
    public_title = forms.CharField(required=False,
                                   label=_('Public Title'),
                                   max_length=2000,
                                   widget=forms.Textarea)
    # TRDS 9b
    acronym = forms.CharField(required=False, label=_('Acronym'),
                              max_length=255)

class SecondaryIdForm(ReviewModelForm):
    class Meta:
        queryset = TrialNumber.objects.all()
        min_required = 0
        polyglot = False
    title = _('Secondary Identifying Numbers')
    # this is just to inherit the custom _html_output and as_table methods

trial_validator.register(TRIAL_FORMS[0], [TrialIdentificationForm, SecondaryIdForm])

### step_2 #####################################################################
class PrimarySponsorForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['primary_sponsor']
        
    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', None)
        super(PrimarySponsorForm, self).__init__(*args, **kwargs)
        if queryset:
            self.fields['primary_sponsor'].queryset = queryset

    title = _('Primary Sponsor')

def make_secondary_sponsor_form(user=None):
    class SecondarySponsorForm(ReviewModelForm):
        class Meta:
            model = TrialSecondarySponsor
            queryset = TrialSecondarySponsor.objects.all()
            min_required = 0
            polyglot = False
            fields = ['institution','relation']

        title = _('Secondary Sponsor(s)')
        if user:
            institution = forms.ModelChoiceField(queryset=Institution.objects.filter(creator=user).order_by('name'),
                                                 label=_('Institution'))
        relation = forms.CharField(widget=forms.HiddenInput, initial=choices.INSTITUTIONAL_RELATION[1][0])
    
    return SecondarySponsorForm

def make_support_source_form(user=None):
    class SupportSourceForm(ReviewModelForm):
        class Meta:
            model = TrialSupportSource
            queryset = TrialSupportSource.objects.all()
            min_required = 0
            polyglot = False
            fields = ['institution','relation']

        title = _('Source(s) of Monetary or Material Support')
        if user:
            institution = forms.ModelChoiceField(queryset=Institution.objects.filter(creator=user).order_by('name'),
                                                 label=_('Institution'))
        relation = forms.CharField(widget=forms.HiddenInput, initial=choices.INSTITUTIONAL_RELATION[0][0])
        
    return SupportSourceForm

trial_validator.register(TRIAL_FORMS[1], [PrimarySponsorForm, make_secondary_sponsor_form(), make_support_source_form()])



### step_3 #####################################################################
class HealthConditionsForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['hc_freetext',]

    title = _('Health Condition(s) or Problem(s) Studied')

    # TRDS 12a
    hc_freetext = forms.CharField(label=_('Health Condition(s) or Problem(s)'),
                                         required=False, max_length=8000,
                                         widget=forms.Textarea)

class GeneralHealthDescriptorForm(ReviewModelForm):
    class Meta:
        model = Descriptor
        queryset = Descriptor.objects.filter(aspect=choices.TRIAL_ASPECT[0][0],level=choices.DESCRIPTOR_LEVEL[0][0])
        min_required = 1
        polyglot = False
        exclude = ['trial','version']
    title = _('General Descriptors for Health Condition(s)')
    aspect = forms.CharField(widget=forms.HiddenInput,
                              initial=choices.TRIAL_ASPECT[0][0])
    level = forms.CharField(widget=forms.HiddenInput,
                              initial=choices.DESCRIPTOR_LEVEL[0][0])

class SpecificHealthDescriptorForm(ReviewModelForm):
    class Meta:
        model = Descriptor
        queryset = Descriptor.objects.filter(aspect=choices.TRIAL_ASPECT[0][0],level=choices.DESCRIPTOR_LEVEL[1][0])
        min_required = 1
        polyglot = False
        exclude = ['trial','version']
    title = _('Specific Descriptors for Health Condition(s)')
    aspect = forms.CharField(widget=forms.HiddenInput,
                              initial=choices.TRIAL_ASPECT[0][0])
    level = forms.CharField(widget=forms.HiddenInput,
                             initial=choices.DESCRIPTOR_LEVEL[1][0])

trial_validator.register(TRIAL_FORMS[2], [HealthConditionsForm, GeneralHealthDescriptorForm, SpecificHealthDescriptorForm])

### step_4 #####################################################################
class InterventionDescriptorForm(ReviewModelForm):
    class Meta:
        model = Descriptor
        queryset = Descriptor.objects.filter(aspect=choices.TRIAL_ASPECT[1][0],
                                            level=choices.DESCRIPTOR_LEVEL[0][0])
        min_required = 1
        polyglot = False
        exclude = ['trial','version']
    title = _('Descriptor for Intervention(s)')
    aspect = forms.CharField(widget=forms.HiddenInput,
                              initial=choices.TRIAL_ASPECT[1][0])
    level = forms.CharField(widget=forms.HiddenInput,
                             initial=choices.DESCRIPTOR_LEVEL[0][0]) # TODO: Change to DESCRIPTOR_LEVEL[1][0]

class InterventionForm(ReviewModelForm):
    title = _('Intervention(s)')
    class Meta:
        model = ClinicalTrial
        fields = ['i_freetext','i_code']
    title = _('Intervention(s)')

    i_freetext = forms.CharField(label=_('Intervention(s)'),
                                         required=False, max_length=8000,
                                         widget=forms.Textarea)

    i_code = forms.ModelMultipleChoiceField(label=_("Intervention Code(s)"),
                                            queryset=InterventionCode.objects.all(),
                                            widget=forms.CheckboxSelectMultiple())

trial_validator.register(TRIAL_FORMS[3], [InterventionForm, InterventionDescriptorForm])

### step_5 #####################################################################
class RecruitmentForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['recruitment_status', 'recruitment_country','enrollment_start_planned',
                  'enrollment_end_planned','target_sample_size', 'inclusion_criteria',
                  'gender', 'agemin_value', 'agemin_unit',
                  'agemax_value', 'agemax_unit', 'exclusion_criteria',
                  ]

    title = _('Recruitment')

    # TRDS 18
    recruitment_status = MultilingualModelChoiceField(
            label=_('Study Status'),
            initial=RecruitmentStatus.objects.get(pk=1),
            model=RecruitmentStatus,
            label_field='label',
            )

    recruitment_country = MultilingualModelMultipleChoiceField(
            label=_('Recruitment Country'),
            model=CountryCode,
            label_field='description',
            )

    # TRDS 16a,b (type_enrollment: anticipated or actual)
    enrollment_start_planned = forms.DateField( # yyyy-mm or yyyy-mm-dd
        required=False,
        label=_('Planned Date of First Enrollment'))

    # TRDS 17
    target_sample_size = forms.IntegerField(label=_('Target Sample Size'),
                                             initial=0 , required=False)
    # TRDS 14a
    inclusion_criteria = forms.CharField(label=_('Inclusion Criteria'),
                                         required=False, max_length=8000,
                                         widget=forms.Textarea)
    # TRDS 14b
    gender = forms.ChoiceField(label=_('Gender (inclusion sex)'),
                               choices=choices.INCLUSION_GENDER)
    # TRDS 14c
    agemin_value = forms.IntegerField(required=False, label=_('Inclusion Minimum Age'))

    agemin_unit = forms.ChoiceField(label=_('Minimum Age Unit'),
                                   choices=choices.INCLUSION_AGE_UNIT)
    # TRDS 14d
    agemax_value = forms.IntegerField(required=False, label=_('Inclusion Maximum Age'))

    agemax_unit = forms.ChoiceField(label=_('Maximum Age Unit'),
                                   choices=choices.INCLUSION_AGE_UNIT)
    # TRDS 14e
    exclusion_criteria = forms.CharField(label=_('Exclusion Criteria'),required=False,
                                        max_length=8000, widget=forms.Textarea,)

trial_validator.register(TRIAL_FORMS[4], [RecruitmentForm])

### step_6 #####################################################################
class StudyTypeForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['study_design',
                  'expanded_access_program',
                  'purpose',
                  'intervention_assignment',
                  'number_of_arms',
                  'masking',
                  'allocation',
                  'phase']

    title = _('Study Type')

    # TRDS 15b
    study_design = forms.CharField(label=_('Study Design'),
                                         required=False, max_length=1000,
                                         widget=forms.Textarea)

    # TRDS 15c
    phase = forms.ModelChoiceField(label=_('Study Phase'),
                                   required=False,
                                   queryset=StudyPhase.objects.all())
                                   
    expanded_access_program = forms.ChoiceField(label=_('Expanded access program'),
                                              required=False,
                                              choices=[(None,_('Unknown')),
                                                       (True,_('Yes')),
                                                       (False,_('No')),])

trial_validator.register(TRIAL_FORMS[5], [StudyTypeForm])

### step_7 #####################################################################
class PrimaryOutcomesForm(ReviewModelForm):
    class Meta:
        model = Outcome
        queryset = Outcome.objects.filter(interest=choices.OUTCOME_INTEREST[0][0])
        min_required = 1
        polyglot = True
        polyglot_fields = ['description']
        fields = ['description','interest']

    title = _('Primary Outcomes')
    interest = forms.CharField(initial=choices.OUTCOME_INTEREST[0][0],
                               widget=forms.HiddenInput)

class SecondaryOutcomesForm(ReviewModelForm):
    class Meta:
        model = Outcome
        queryset = Outcome.objects.filter(interest=choices.OUTCOME_INTEREST[1][0])
        min_required = 0
        polyglot = True
        polyglot_fields = ['description']
        fields = ['description','interest']

    title = _('Secondary Outcomes')
    interest = forms.CharField(initial=choices.OUTCOME_INTEREST[1][0],
                               widget=forms.HiddenInput)

trial_validator.register(TRIAL_FORMS[6], [PrimaryOutcomesForm,SecondaryOutcomesForm])

### step_8 #####################################################################
def make_public_contact_form(user=None):
    class PublicContactForm(ReviewModelForm):
        class Meta:
            model = ClinicalTrial
            queryset = PublicContact.objects.all()
            min_required = 0
            polyglot = False
            fields = ['contact']

        title = _('Contact(s) for Public Queries')
        relation = forms.CharField(label=_('Relation'), 
                                   initial=choices.CONTACT_RELATION[0][0],
                                   widget=forms.HiddenInput)
        if user:
            contact = forms.ModelChoiceField(queryset=Contact.objects.filter(creator=user).order_by('firstname', 'middlename', 'lastname'),
                                                 label=_('Contact'))
    return PublicContactForm

def make_scientifc_contact_form(user=None):
    class ScientificContactForm(ReviewModelForm):
        class Meta:
            model = ClinicalTrial
            queryset = ScientificContact.objects.all()
            min_required = 1
            polyglot = False
            fields = ['contact']

        title = _('Contact(s) for Scientific Queries')
        relation = forms.CharField(label=_('Relation'), 
                                   initial=choices.CONTACT_RELATION[1][0],
                                   widget=forms.HiddenInput)
        if user:
            contact = forms.ModelChoiceField(queryset=Contact.objects.filter(creator=user).order_by('firstname', 'middlename', 'lastname'),
                                                 label=_('Contact'))
    return ScientificContactForm

def make_site_contact_form(user=None):
    class SiteContactForm(ReviewModelForm):
        class Meta:
            model = ClinicalTrial
            queryset = SiteContact.objects.all()
            min_required = 1
            polyglot = False
            fields = ['contact']

        title = _('Contact(s) for Site Queries')
        relation = forms.CharField(label=_('Relation'), 
                                   initial=choices.CONTACT_RELATION[2][0],
                                   widget=forms.HiddenInput)
        if user:
            contact = forms.ModelChoiceField(queryset=Contact.objects.filter(creator=user).order_by('firstname', 'middlename', 'lastname'),
                                                 label=_('Contact'))
    return SiteContactForm

trial_validator.register(TRIAL_FORMS[7], [make_public_contact_form(),make_scientifc_contact_form(),make_scientifc_contact_form()])

#step8-partof
# http://www.b-list.org/weblog/2008/nov/09/dynamic-forms/
# http://stackoverflow.com/questions/622982/django-passing-custom-form-parameters-to-formset
def make_contact_form(user):
    class ContactForm(ReviewModelForm):
        class Meta:
            model = Contact
            
        def __init__(self, *args, **kwargs):
            super(ReviewModelForm, self).__init__(*args, **kwargs)
            self.fields.insert(0, 'relation', forms.ChoiceField(label=_('Contact Type'), 
                                   widget=forms.RadioSelect,
                                   choices=choices.CONTACT_RELATION))

        title = _('New Contact(s)')

        firstname = forms.CharField(label=_('First Name'), max_length=50)
        middlename = forms.CharField(label=_('Middle Name'), max_length=50,required=False)
        lastname = forms.CharField(label=_('Last Name'), max_length=50)

        email = forms.EmailField(label=_('E-mail'), max_length=255)

        affiliation = forms.ModelChoiceField(queryset=Institution.objects.filter(creator=user).order_by('name'),
                                             label=_('Institution'))

        address = forms.CharField(label=_('Address'), max_length=255,required=False, 
                                  widget=forms.TextInput(attrs={'style': 'width:400px;'}))
        city = forms.CharField(label=_('City'), max_length=255)

        country = forms.ModelChoiceField(CountryCode.objects.all(),
                                         label=_('Country'))

        zip = forms.CharField(label=_('Postal Code'), max_length=50)
        telephone = forms.CharField(label=_('Telephone'), max_length=255)
        
    return ContactForm

class NewInstitution(ReviewModelForm):
    class Meta:
        model = Institution

    title = _('New Institution')
