#coding: utf-8

from assistance.models import FieldHelp
from vocabulary.models import CountryCode
from repository.models import ClinicalTrial, Contact, Descriptor, Institution
from repository.models import InterventionCode, Outcome, RecruitmentStatus
from repository.models import StudyPhase, TrialSecondarySponsor
from repository.models import TrialSupportSource

import choices

from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django import forms
from django.forms.forms import BoundField, conditional_escape

class ReviewModelForm(forms.ModelForm):
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
                    label = bf.label_tag(label) or ''
                else:
                    label = ''
                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = u''
                form_name = self.__class__.__name__
                #import pdb; pdb.set_trace()
                help_record, new = FieldHelp.objects.get_or_create(form=form_name, field=name)
                help_text = help_text + u' ' + force_unicode(help_record)
                help_text = help_text_html % help_text
                field_path = '%s.%s' % (form_name, name)
                issue_text = '%s #%s' % (field_path, self.instance.pk)
                output.append(normal_row % {'errors': force_unicode(bf_errors),
                                            'label': force_unicode(label),
                                            'field': unicode(bf),
                                            'help_text': help_text,
                                            'help_id': 'id_%s-help%s' % ((self.prefix or name),help_record.pk),
                                            'issue': issue_text,})
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
            <tr><th>%(label)s</th>
                <td>%(errors)s%(field)s</td>
                <td class="help">
                    <img src="/static/help.png" rel="#%(help_id)s"/>
                    <div id="%(help_id)s" class="help">%(help_text)s</div>
                    <div class="issue">%(issue)s</div>
                    </td></tr>
        '''
        return self._html_output(normal_row=normal_row,
                                 error_row=u'<tr><td colspan="3">%s</td></tr>',
                                 row_ender='</td></tr>',
                                 help_text_html=u'%s',
                                 errors_on_separate_row=False)
#
# Forms
#

#step1
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
    title = _('Secondary Identifying Numbers')
    # this is just to inherit the custom _html_output and as_table methods


#step2
class PrimarySponsorForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['primary_sponsor',]

    title = _('Primary Sponsor')

#step2
class SecondarySponsorForm(ReviewModelForm):
    class Meta:
        model = TrialSecondarySponsor
        fields = ['institution','relation']

    title = _('Secondary Sponsor(s)')
    relation = forms.CharField(widget=forms.HiddenInput, initial=choices.INSTITUTIONAL_RELATION[1][0])

#step2
class SupportSourceForm(ReviewModelForm):
    class Meta:
        model = TrialSupportSource
        fields = ['institution','relation']

    title = _('Source(s) of Monetary or Material Support')
    relation = forms.CharField(widget=forms.HiddenInput, initial=choices.INSTITUTIONAL_RELATION[0][0])

class NewInstitution(ReviewModelForm):
    class Meta:
        model = Institution

    title = _('New Institution')

#step3
class HealthConditionsForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['hc_freetext',]

    title = _('Health Condition(s) or Problem(s) Studied')

    # TRDS 12a
    hc_freetext = forms.CharField(label=_('Health Condition(s) or Problem(s)'),
                                         required=False, max_length=8000,
                                         widget=forms.Textarea)

#step3
class DescriptorForm(ReviewModelForm):
    class Meta:
        model = Descriptor
        exclude = ['trial','version']
        
        
class GeneralHealthDescriptorForm(DescriptorForm):
    title = _('General Descriptors for Health Condition(s)')
    aspect = forms.CharField(widget=forms.HiddenInput,
                              initial=choices.TRIAL_ASPECT[0][0])
    level = forms.CharField(widget=forms.HiddenInput,
                              initial=choices.DESCRIPTOR_LEVEL[0][0])

class SpecificHealthDescriptorForm(DescriptorForm):
    title = _('Specific Descriptors for Health Condition(s)')
    aspect = forms.CharField(widget=forms.HiddenInput,
                              initial=choices.TRIAL_ASPECT[0][0])
    level = forms.CharField(widget=forms.HiddenInput,
                             initial=choices.DESCRIPTOR_LEVEL[1][0])

#step4
class InterventionDescriptorForm(DescriptorForm):
    title = _('Descriptor for Intervention(s)')
    aspect = forms.CharField(widget=forms.HiddenInput,
                              initial=choices.TRIAL_ASPECT[1][0])
    level = forms.CharField(widget=forms.HiddenInput,
                             initial=choices.DESCRIPTOR_LEVEL[0][0])

#step4
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
#step5
class RecruitmentForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['recruitment_status', 'recruitment_country','enrollment_start_planned',
                  'target_sample_size', 'inclusion_criteria', 'gender',
                  'agemin_value', 'agemin_unit',
                  'agemax_value', 'agemax_unit', 'exclusion_criteria',
                  ]

    title = _('Recruitment')

    # TRDS 18
    recruitment_status = forms.ModelChoiceField(label=_('Recruitment Status'),
                                                queryset=RecruitmentStatus.objects.all())

    recruitment_country = forms.ModelMultipleChoiceField(
                                            label=_('Recruitment Country'),
                                            queryset=CountryCode.objects.all())

    # TRDS 16a,b (type_enrollment: anticipated or actual)
    enrollment_start_planned = forms.DateField( # yyyy-mm or yyyy-mm-dd
        label=_('Planned Date of First Enrollment'), required=False)

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

#step6
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
    expanded_access_program = forms.ChoiceField(label=_('Expandend Access Program'),
                                              choices=[(None,_('Unknown')),
                                                       (True,_('Yes')),
                                                       (False,_('No')),],
                                              widget=forms.RadioSelect)

    # TRDS 15c
    phase = forms.ModelChoiceField(label=_('Study Phase'),
                                   queryset=StudyPhase.objects.all())

#step7
class PrimaryOutcomesForm(ReviewModelForm):
    class Meta:
        model = Outcome
        fields = ['interest','description']

    title = _('Primary Outcomes')
    interest = forms.CharField(initial=choices.OUTCOME_INTEREST[0][0],
                               widget=forms.HiddenInput)

class SecondaryOutcomesForm(ReviewModelForm):
    class Meta:
        model = Outcome
        fields = ['interest','description']

    title = _('Secondary Outcomes')
    interest = forms.CharField(initial=choices.OUTCOME_INTEREST[1][0],
                               widget=forms.HiddenInput)

#step8
class PublicContactForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['contact']

    title = _('Contact(s) for Public Queries')
    relation = forms.CharField(initial=choices.CONTACT_RELATION[0][0],
                               widget=forms.HiddenInput)

#step8
class ScientificContactForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['contact']

    title = _('Contact(s) for Scientific Queries')
    relation = forms.CharField(initial=choices.CONTACT_RELATION[1][0],
                               widget=forms.HiddenInput)

#step8
class SiteContactForm(ReviewModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['contact']

    title = _('Contact(s) for Site Queries')
    relation = forms.CharField(initial=choices.CONTACT_RELATION[2][0],
                               widget=forms.HiddenInput)

#step8-partof
class ContactForm(ReviewModelForm):
    class Meta:
        model = Contact

    title = _('New Contact(s)')
    relation = forms.ChoiceField(widget=forms.RadioSelect,
                               choices=choices.CONTACT_RELATION)

    firstname = forms.CharField(label=_('First Name'), max_length=50)
    middlename = forms.CharField(label=_('Middle Name'), max_length=50,required=False)
    lastname = forms.CharField(label=_('Last Name'), max_length=50)

    email = forms.EmailField(label=_('E-mail'), max_length=255)

    affiliation = forms.ModelChoiceField(Institution.objects.all(),
                                         _('Affiliation'))

    address = forms.CharField(label=_('Address'), max_length=255,required=False)
    city = forms.CharField(label=_('City'), max_length=255)

    country = forms.ModelChoiceField(CountryCode.objects.all(), _('Country'))

    zip = forms.CharField(label=_('Postal Code'), max_length=50)
    telephone = forms.CharField(label=_('Telephone'), max_length=255)