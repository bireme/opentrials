# coding: utf-8
from tempfile import NamedTemporaryFile
import lxml
import re

from opentrials.repository.trds_forms import ReviewModelForm
from opentrials.reviewapp.models import Remark
from opentrials.reviewapp.models import UserProfile
from opentrials.reviewapp.models import Attachment, Submission
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.conf import settings
from django.forms.formsets import formset_factory, BaseFormSet

from polyglot.multilingual_forms import MultilingualBaseForm
from polyglot.multilingual_forms import MultilingualModelChoiceField, MultilingualModelMultipleChoiceField

from repository.models import Institution, CountryCode, ClinicalTrial
from repository.widgets import SelectInstitution
from repository.xml.validate import validate_xml, InvalidOpenTrialsXML, ICTRP_DTD
from repository.xml.loading import etree, OpenTrialsXMLImport, REPLACE_IF_EXISTS
from repository.trds_forms import utrn_number_validate

ACCESS = [
    ('public', 'Public'),
    ('private', 'Private'),
]


class InitialTrialForm(ReviewModelForm):
    class Meta:
        model = Submission
        exclude = ['trial', 'status', 'staff_note', 'title']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        self.base_fields.keyOrder = ['language', 'scientific_title', 'recruitment_country',
                'utrn_number', 'primary_sponsor',]

        self.base_fields['primary_sponsor'] = forms.ModelChoiceField(queryset=Institution.objects.filter(creator=self.user).order_by('name'),
                                                label=_('Primary Sponsor'),
                                                widget=SelectInstitution(formset_prefix='primary_sponsor'),
                                                required=True)

        super(InitialTrialForm, self).__init__(*args, **kwargs)

        self.fields['language'] = forms.ChoiceField(label=_('Submission language'),
                    choices=settings.MANAGED_LANGUAGES_CHOICES,
                    initial=self.user.get_profile().preferred_language)

    form_title = _('Initial Trial Data')
    scientific_title = forms.CharField(widget=forms.Textarea,
                                       label=_('Scientific Title'),
                                       max_length=2000)
    recruitment_country = MultilingualModelMultipleChoiceField(
                                                    label=_('Recruitment Country'),
                                                    model=CountryCode,
                                                    label_field='description',)
    utrn_number = forms.CharField(label=_('UTN Number'), max_length=255, required=True)
    language = forms.ChoiceField(label=_('Submission language'),
                                 choices=settings.MANAGED_LANGUAGES_CHOICES)

    def clean_utrn_number(self):
        data = utrn_number_validate(self.cleaned_data['utrn_number'].strip())
        if ClinicalTrial.objects.filter(utrn_number=data).count() > 0:
            raise forms.ValidationError(_('UTN number already exists.'))
        return data

class PrimarySponsorForm(ReviewModelForm):
    class Meta:
        model = Institution
        exclude = ['address']
    form_title = _('Primary Sponsor')

    country = MultilingualModelChoiceField(
            label=_('Country'),
            queryset=CountryCode.objects.all(),
            required=True,
            label_field='description',)

class ExistingAttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        exclude = ['submission']

    title = _('Existing Attachment')
    file = forms.CharField(required=False,label=_('File'),max_length=255)

class NewAttachmentForm(ReviewModelForm):
    UPLOAD_CHOICES = [['file',_('File')],['url',_('URL Link')]]

    attach_type = forms.ChoiceField(label=_('Attachment Type'), 
                                    choices=UPLOAD_CHOICES,
                                    initial='file')
    class Meta:
        model = Attachment
        fields = ['attach_type', 'file', 'attach_url','description','public',]
        widgets = {
                    'attach_url': forms.widgets.Input(attrs={'disabled': 'true'}),
                  }

    title = _('New Attachment')

    def clean(self):
        cleaned_data = super(NewAttachmentForm,self).clean()
        upload_file = cleaned_data.get('attach_type') == 'file'
        if upload_file:
            if not cleaned_data.get('file'):
                raise forms.ValidationError(_("Choose one file to upload"))
        else:
            if not cleaned_data.get('attach_url'):
                raise forms.ValidationError(_("Place one URL address"))
        
        return cleaned_data


class UserForm(forms.ModelForm):
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if self.cleaned_data['email'] != self.instance.email:
            if User.objects.filter(email__iexact=self.cleaned_data['email']):
                raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['first_name','last_name','email']

    title = _('User Profile')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['preferred_language']

    title = _('Aditional info for profile')

class UploadTrialForm(forms.Form):
    submission_file = forms.Field(widget=forms.FileInput, required=True)

    xml_format = 'opentrials'

    def clean_submission_file(self):
        submission_file = self.cleaned_data['submission_file']

        # This is a XML file
        try:
            self.tree = etree.parse(submission_file)
        except etree.XMLSyntaxError:
            raise forms.ValidationError(_('Invalid XML syntax.'))

        # Runs DTD validation for OpenTrials XML
        try:
            validate_xml(self.tree)
            self.xml_format = 'opentrials'
        except InvalidOpenTrialsXML:
            try:
                validate_xml(self.tree, dtd=ICTRP_DTD)
                self.xml_format = 'ictrp'
            except InvalidOpenTrialsXML:
                raise forms.ValidationError('Invalid file or not detected format.')

        return submission_file

    def parse_file(self, user, xml_format=None):
        xml_format = xml_format or self.xml_format
        imp = OpenTrialsXMLImport(creator=user)

        if xml_format == 'opentrials':
            return imp.parse_opentrials(self.tree)
        else:
            return imp.parse_ictrp(self.tree)

class ImportParsedForm(forms.Form):
    trial_id = forms.Field(widget=forms.HiddenInput)
    description = forms.Field(widget=forms.HiddenInput, required=False)
    to_import = forms.BooleanField(required=False)

class BaseImportParsedFormset(BaseFormSet):
    def import_file(self, parsed_trials, user):
        imp = OpenTrialsXMLImport(creator=user)

        imp._parsed_trials = parsed_trials

        return imp.import_parsed(if_exists=REPLACE_IF_EXISTS)

ImportParsedFormset = formset_factory(ImportParsedForm, formset=BaseImportParsedFormset, extra=0)

class OpenRemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        exclude = ['submission','context','status']

    title = _('Open a new Remark')

class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super(ContactForm, self).__init__(*args, **kwargs)

        if self.user:
            self.fields['name'] = forms.CharField(label=_("Name"), max_length=50, initial=self.user.first_name)
            self.fields['from_email'] = forms.EmailField(label=_("E-mail"), initial=self.user.email)

    name = forms.CharField(label=_("Name"), max_length=50)
    from_email = forms.EmailField(label=_("E-mail"))
    subject = forms.CharField(label=_("Subject"), max_length=50)
    message = forms.CharField(label=_("Message"), widget=forms.Textarea)

class TermsUseForm(forms.Form):
    agree = forms.BooleanField(label=_("I read and agree to all terms above"), required=True,
                               error_messages={'required': _('You must agree to the terms')})

class ResendActivationEmail(forms.Form):
    email = forms.EmailField(label=_("E-mail"))
