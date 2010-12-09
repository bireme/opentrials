# coding: utf-8

from opentrials.repository.trds_forms import ReviewModelForm
from opentrials.reviewapp.models import Remark
from opentrials.reviewapp.models import UserProfile
from opentrials.reviewapp.models import Attachment, Submission
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings

from polyglot.multilingual_forms import MultilingualBaseForm
from polyglot.multilingual_forms import MultilingualModelChoiceField, MultilingualModelMultipleChoiceField

from repository.models import Institution, CountryCode
from repository.widgets import SelectInstitution

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
                'primary_sponsor',]

        super(InitialTrialForm, self).__init__(*args, **kwargs)

        self.fields['primary_sponsor'].queryset = Institution.objects.order_by('name')
        self.fields['primary_sponsor'].widget = SelectInstitution(formset_prefix='primary_sponsor')

        if self.user:
            self.fields['language'] = forms.ChoiceField(label=_('Submission language'), 
                        choices=settings.MANAGED_LANGUAGES_CHOICES, 
                        initial=self.user.get_profile().preferred_language)
            self.fields['primary_sponsor'].queryset = self.fields['primary_sponsor'].queryset.filter(creator=self.user)

    form_title = _('Initial Trial Data')
    scientific_title = forms.CharField(widget=forms.Textarea, 
                                       label=_('Scientific Title'), 
                                       max_length=2000)
    recruitment_country = MultilingualModelMultipleChoiceField(
                                                    label=_('Recruitment Country'),
                                                    model=CountryCode,
                                                    label_field='description',)
    language = forms.ChoiceField(label=_('Submission language'), 
                                 choices=settings.MANAGED_LANGUAGES_CHOICES)

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
    class Meta:
        model = Attachment
        fields = ['file','description','public']

    title = _('New Attachment')
    
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

class UploadTrial(forms.Form):
    submission_xml = forms.CharField(widget=forms.FileInput,required=True)

class OpenRemarkForm(forms.ModelForm):
    class Meta:
        model = Remark
        exclude = ['submission','context','status']

    title = _('Open a new Remark')
    
class ContactForm(forms.Form):
    name = forms.CharField(label=_("Name"), max_length=50)
    from_email = forms.EmailField(label=_("E-mail"))
    subject = forms.CharField(label=_("Subject"), max_length=50)
    message = forms.CharField(label=_("Message"), widget=forms.Textarea)

class TermsUseForm(forms.Form):
    agree = forms.BooleanField(label=_("I read and agree to all terms above"), required=True, 
                               error_messages={'required': _('You must agree to the terms')})

