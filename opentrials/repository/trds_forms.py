#coding: utf-8

from assistance.models import FieldHelp, FieldHelpTranslation
from repository.models import ClinicalTrial, Contact, Descriptor, Institution
from repository.models import Outcome, TrialNumber
from repository.models import TrialSecondarySponsor, TrialSupportSource
from repository.models import SiteContact, PublicContact, ScientificContact
from vocabulary.models import CountryCode, StudyPhase, StudyType, RecruitmentStatus
from vocabulary.models import InterventionCode, StudyMasking, StudyAllocation
from vocabulary.models import TimePerspective, ObservationalStudyDesign
from vocabulary.models import StudyPurpose, InterventionAssigment, InstitutionType
from repository.widgets import SelectWithLink, SelectInstitution, YearMonthWidget

import choices

from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, get_language
from django.forms.formsets import DELETION_FIELD_NAME
from django.template.defaultfilters import linebreaksbr

from django import forms
from django.forms.forms import BoundField, conditional_escape

from polyglot.multilingual_forms import MultilingualCharField, MultilingualTextField
from polyglot.multilingual_forms import MultilingualModelChoiceField, MultilingualModelMultipleChoiceField
from polyglot.multilingual_forms import MultilingualBaseForm, MultilingualBaseFormSet
from polyglot.multilingual_forms import MultilingualModelCheckboxField

from trial_validation import trial_validator, TRIAL_FORMS

from datetime import date
import datetime
import re

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
                    if hasattr(self.Meta,'min_required'):
                        if not hasattr(self.Meta,'count'):
                            self.Meta.count = 0
                        if self.Meta.min_required > 0 and self.Meta.count < self.Meta.min_required:
                            if name != 'DELETE':
                                label = label + ' <span class="required_field">(*)</span>'
                    elif trial_validator.field_is_required(self, name):
                        label = label + ' <span class="required_field">(*)</span>'
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
                help_record, new = FieldHelp.objects.get_or_create(form=form_name, field=name)

                # Trying to get the translation for help_record
                try:
                    help_object = FieldHelpTranslation.objects.get_translation_for_object(
                        lang=get_language(), model=FieldHelp, object_id=help_record.pk,
                        )
                    help_text = "<div class='help_text'>%s</div>" % (help_object.text,)
                    if help_object.example:
                        help_text = "%s<div class='help_text_example'>%s:<br />%s</div>" % (help_text, _("Example"), help_object.example)

                    if not help_text.strip():
                        help_text = unicode(help_record)
                except (FieldHelpTranslation.DoesNotExist, AttributeError):
                    help_text = "<div class='help_text'>%s</div>" % (help_record.text,)
                    if help_record.example:
                        help_text = "%s<div class='help_text_example'>%s:<br />%s</div>" % (help_text, _("Example"), help_record.example)

                help_text = u'' + force_unicode(help_text)
                help_text = linebreaksbr(help_text_html % help_text)
                output.append(normal_row % {'errors': force_unicode(bf_errors),
                                            'label': force_unicode(label),
                                            'field': unicode(bf),
                                            'help_text': help_text,
                                            'help_id': 'id_%s-help%s' % ((self.prefix or name),help_record.pk),
                                            'field_class': field_status,
                                            'field_name': name,
                                            })

        # if necessary, updates the count of rendered repetitive forms
        if hasattr(self.Meta,'min_required'):
            if hasattr(self.Meta,'count'):
                self.Meta.count = self.Meta.count + 1

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
            <tr class="%(field_class)s %(field_name)s"><th><img src="/static/help.png" rel="#%(help_id)s"/>
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

def utrn_number_validate(data):
    if data:
        if not re.match('^U\d{4}-\d{4}-\d{4}$', data):
            raise forms.ValidationError(_("Invalid format. Example: U1111-1111-1111"))
    return data

### step_1 #####################################################################
class TrialIdentificationForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['scientific_title','scientific_acronym',
                  'scientific_acronym_expansion','public_title',
                  'acronym','acronym_expansion','utrn_number']

    title = _('Trial Identification')
    # TRDS 10a
    scientific_title = forms.CharField(required=True,
                                       label=_('Scientific Title'),
                                       max_length=2000,
                                       widget=forms.Textarea)
    # TRDS 10b
    scientific_acronym = forms.CharField(required=False,
                                         label=_('Scientific Acronym'),
                                         max_length=255)
    # TRDS 9a
    public_title = forms.CharField(required=True,
                                   label=_('Public Title'),
                                   max_length=2000,
                                   widget=forms.Textarea)
    # TRDS 9b
    acronym = forms.CharField(required=False, label=_('Acronym'),
                              max_length=255)

    def clean_utrn_number(self):
        data = utrn_number_validate(self.cleaned_data['utrn_number'].strip())
        if ClinicalTrial.objects.filter(utrn_number=data).exclude(pk=self.instance.pk).count() > 0:
            raise forms.ValidationError(_('UTN number already exists.'))
        return data


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
            min_required = 1
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
            min_required = 1
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

    i_code = MultilingualModelCheckboxField(
                label=_("Intervention Code(s)"),
                model=InterventionCode,
                label_field='label',
            )

trial_validator.register(TRIAL_FORMS[3], [InterventionForm, InterventionDescriptorForm])

### step_5 #####################################################################
class RecruitmentForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['recruitment_status', 'recruitment_country',
                  'target_sample_size', 'inclusion_criteria',
                  'gender', 'agemin_value', 'agemin_unit',
                  'agemax_value', 'agemax_unit', 'exclusion_criteria',
                  ]

    title = _('Recruitment')

    # TRDS 18
    recruitment_status = MultilingualModelChoiceField(
            label=_('Study Status'),
            queryset=RecruitmentStatus.objects.all(),
            required=False,
            label_field='label',
            )

    recruitment_country = MultilingualModelMultipleChoiceField(
            label=_('Recruitment Country'),
            model=CountryCode,
            label_field='description',
            )
    from django.forms.extras.widgets import SelectDateWidget
    # TRDS 16a,b (type_enrollment: anticipated or actual)
    year = date.today().year
    enrollment_start_date = forms.DateField(
        required=False,
        label=_('Date of First Enrollment'),
        widget=SelectDateWidget(years=[y for y in range(year-1, year+50)]),
        )
    enrollment_end_date = forms.DateField(
        required=False,
        label=_('Date of Last Enrollment'),
        widget=SelectDateWidget(years=[y for y in range(year-1, year+50)]),
        )

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

    def clean_enrollment_end_date(self):
        if self.cleaned_data.get('recruitment_status'):
            if self.cleaned_data.get('recruitment_status').label == unicode(_('recruiting')):
                if self.cleaned_data.get('enrollment_end_date', None) is None:
                    raise forms.ValidationError(_("Recruiting trial requires an end date"))

        end_date = self.cleaned_data.get('enrollment_end_date')
        return end_date

    def clean_enrollment_start_date(self):
        if self.cleaned_data.get('recruitment_status'):
            if self.cleaned_data.get('recruitment_status').label == unicode(_('recruiting')):
                if self.cleaned_data.get('enrollment_start_date', None) is None:
                    raise forms.ValidationError(_("Recruiting trial requires a start date"))

        start_date = self.cleaned_data.get('enrollment_start_date')
        return start_date

    def __init__(self, *args, **kwargs):
        self.base_fields.keyOrder = ['recruitment_status', 'recruitment_country',
                'enrollment_start_date', 'enrollment_end_date', 'target_sample_size',
                'inclusion_criteria', 'gender', 'agemin_value', 'agemin_unit',
                'agemax_value', 'agemax_unit', 'exclusion_criteria']

        super(RecruitmentForm, self).__init__(*args, **kwargs)

        if self.instance:

            date = self.instance.enrollment_start_planned or self.instance.enrollment_start_actual
            if date:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                self.fields['enrollment_start_date'].initial = date
            
            date = self.instance.enrollment_end_planned or self.instance.enrollment_end_actual
            if date:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                self.fields['enrollment_end_date'].initial = date

    def save(self, commit=True, *args, **kwargs):

        obj = super(RecruitmentForm, self).save(commit=True, *args, **kwargs)
        

        obj.enrollment_start_planned = None
        obj.enrollment_start_actual = None

        if self.cleaned_data.get('enrollment_start_date', None):

            start_date = self.cleaned_data['enrollment_start_date']
            if start_date > date.today():
                obj.enrollment_start_planned = start_date
            else:
                obj.enrollment_start_actual = start_date

        obj.enrollment_end_planned = None
        obj.enrollment_end_actual = None
        if self.cleaned_data.get('enrollment_end_date', None):
            end_date = self.cleaned_data['enrollment_end_date']
            if end_date > date.today():
                obj.enrollment_end_planned = end_date
            else:
                obj.enrollment_end_actual = end_date

        if commit:
            obj.save()

        return obj

    def clean(self):
        cleaned_data = super(RecruitmentForm, self).clean()
        start_date = cleaned_data.get('enrollment_start_date')
        end_date = cleaned_data.get('enrollment_end_date')
        if end_date and start_date and start_date > end_date:
            raise forms.ValidationError(_("Invalid date"))
        
        if cleaned_data.get('agemin_unit') != '-' and cleaned_data.get('agemax_unit') != '-':
            min_age = normalize_age(cleaned_data.get('agemin_value'), cleaned_data.get('agemin_unit'))
            max_age = normalize_age(cleaned_data.get('agemax_value'), cleaned_data.get('agemax_unit'))
            if max_age < min_age:
                raise forms.ValidationError(_("Invalid age limits"))

        return cleaned_data

trial_validator.register(TRIAL_FORMS[4], [RecruitmentForm])

def normalize_age(age, unity):
    "convert ages to hours"
    if unity == 'Y':
        return age*365*24
    elif unity == 'M':
        return age*30*24
    elif unity == 'W':
        return age*7*24
    elif unity == 'D':
        return age*24
    elif unity == 'H':
        return age
    return age
### step_6 #####################################################################
class StudyTypeForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['is_observational',
                  'study_design',
                  'expanded_access_program',
                  'purpose',
                  'intervention_assignment',
                  'number_of_arms',
                  'masking',
                  'allocation',
                  'phase',
                  'observational_study_design',
                  'time_perspective',]

    title = _('Study Type')

    # TRDS 15b
    study_design = forms.CharField(label=_('Study Design'),
                                         required=False, max_length=1000,
                                         widget=forms.Textarea)

    purpose = MultilingualModelChoiceField(
        label=_('Study Purpose'),
        queryset=StudyPurpose.objects.all(),
        required=False,
        label_field='label',
        )

    intervention_assignment = MultilingualModelChoiceField(
        label=_('Intervention Assignment'),
        queryset=InterventionAssigment.objects.all(),
        required=False,
        label_field='label',
        )

    masking = MultilingualModelChoiceField(
        label=_('Masking type'),
        queryset=StudyMasking.objects.all(),
        required=False,
        label_field='label',
        )

    is_observational = forms.ChoiceField(
        label=_('Study Type'),
        required=True,
        choices=[
            (False,_('Intervention')),
            (True,_('Observational')),
        ])

    allocation = MultilingualModelChoiceField(
        label=_('Allocation type'),
        queryset=StudyAllocation.objects.all(),
        required=False,
        label_field='label',
        )

    # TRDS 15c
    phase = MultilingualModelChoiceField(
        label=_('Study Phase'),
        queryset=StudyPhase.objects.all(),
        required=False,
        label_field='label',
        )

    time_perspective = MultilingualModelChoiceField(
        label=_('Time Perspective'),
        queryset=TimePerspective.objects.all(),
        required=True,
        label_field='label',
        )

    observational_study_design = MultilingualModelChoiceField(
        label=_('Observational Study Design'),
        queryset=ObservationalStudyDesign.objects.all(),
        required=True,
        label_field='label',
        )

    expanded_access_program = forms.ChoiceField(
        label=_('Expanded access program'),
        required=False,
        choices=[
            (None,_('Unknown')),
            (True,_('Yes')),
            (False,_('No')),
        ])

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
        min_required = 1
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
            min_required = 1
            polyglot = False
            fields = ['contact']

        title = _('Contact(s) for Public Queries')
        relation = forms.CharField(label=_('Relation'),
                                   initial=choices.CONTACT_RELATION[0][0],
                                   widget=forms.HiddenInput)
        if user:
            contact = forms.ModelChoiceField(queryset=Contact.objects.filter(creator=user).order_by('firstname', 'middlename', 'lastname'),
                                             label=_('Contact'),
                                             widget=SelectWithLink(link='#new_contact', text=_('New Contact')))
        else:
            contact = forms.ModelChoiceField(queryset=Contact.objects.all(),
                                             label=_('Contact'),
                                             widget=SelectWithLink(link='#new_contact', text=_('New Contact')))
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
                                             label=_('Contact'),
                                             widget=SelectWithLink(link='#new_contact', text=_('New Contact')))
        else:
            contact = forms.ModelChoiceField(queryset=Contact.objects.all(),
                                             label=_('Contact'),
                                             widget=SelectWithLink(link='#new_contact', text=_('New Contact')))


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
                                             label=_('Contact'),
                                             widget=SelectWithLink(link='#new_contact', text=_('New Contact')))
        else:
            contact = forms.ModelChoiceField(queryset=Contact.objects.all(),
                                             label=_('Contact'),
                                             widget=SelectWithLink(link='#new_contact', text=_('New Contact')))

    return SiteContactForm

trial_validator.register(TRIAL_FORMS[7], [make_public_contact_form(),make_scientifc_contact_form(),make_scientifc_contact_form()])

#step8-partof
# http://www.b-list.org/weblog/2008/nov/09/dynamic-forms/
# http://stackoverflow.com/questions/622982/django-passing-custom-form-parameters-to-formset

def make_contact_form(user,formset_prefix=''):
    class ContactForm(ReviewModelForm):
        class Meta:
            model = Contact

        def __init__(self, *args, **kwargs):
            super(ContactForm, self).__init__(*args, **kwargs)
            self.fields.insert(0, 'relation', forms.ChoiceField(label=_('Contact Type'),
                                   widget=forms.RadioSelect,
                                   choices=choices.CONTACT_RELATION))

        title = _('New Contact(s)')

        firstname = forms.CharField(label=_('First Name'), max_length=50)
        middlename = forms.CharField(label=_('Middle Name'), max_length=50,required=False)
        lastname = forms.CharField(label=_('Last Name'), max_length=50)

        email = forms.EmailField(label=_('E-mail'), max_length=255)

        affiliation = forms.ModelChoiceField(queryset=Institution.objects.filter(creator=user).order_by('name'),
                                             label=_('Institution'),
                                             widget=SelectInstitution(formset_prefix=formset_prefix))

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

    country = MultilingualModelChoiceField(
                label=_('Country'),
                queryset=CountryCode.objects.all(),
                required=True,
                label_field='description',)

    i_type = MultilingualModelChoiceField(
                label=_('Institution type'),
                queryset=InstitutionType.objects.all(),
                required=False,
                label_field='label',)
