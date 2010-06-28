# coding: utf-8

from clinicaltrials.repository.trds_forms import ReviewModelForm
from clinicaltrials.reviewapp.models import Remark
from clinicaltrials.reviewapp.models import UserProfile
from clinicaltrials.reviewapp.models import Attachment
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings

from repository.models import Institution, CountryCode

ACCESS = [
    ('public', 'Public'),
    ('private', 'Private'),
]


class InitialTrialForm(forms.Form):
    form_title = _('Initial Trial Data')
    scientific_title = forms.CharField(widget=forms.Textarea, 
                                       label=_('Scientific Title'), 
                                       max_length=2000)
    recruitment_country = forms.MultipleChoiceField(
                                label=_('Recruitment country'), 
                                choices=((cc.pk,cc.description) for cc in CountryCode.objects.iterator()))
    language = forms.ChoiceField(label=_('Submission language'), 
                                 choices=settings.MANAGED_LANGUAGES_CHOICES)
    
class PrimarySponsorForm(forms.ModelForm):
    class Meta:
        model = Institution
        exclude = ['address']
    form_title = _('Primary Sponsor')

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

    title = _('Open Remark')
    
class ContactForm(forms.Form):
    name = forms.CharField(label=_("Name"), max_length=50)
    from_email = forms.EmailField(label=_("E-mail"))
    subject = forms.CharField(label=_("Subject"), max_length=50)
    message = forms.CharField(label=_("Message"), widget=forms.Textarea)

