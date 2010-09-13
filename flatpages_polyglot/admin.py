from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AlreadyRegistered
from django import forms

from models import FlatPageTranslation, FlatPage

class FormFlatPageTranslation(forms.ModelForm):
    class Meta:
        model = FlatPageTranslation
        fields = ('language','title','content')

    flatpage = forms.ModelChoiceField(queryset=FlatPage.objects.all())

    def __init__(self, *args, **kwargs):
        super(FormFlatPageTranslation, self).__init__(*args, **kwargs)

        self.fields.keyOrder = ['flatpage','language','title','content']

        if self.instance:
            self.fields['flatpage'].initial = self.instance.content_object.pk

    def save(self, commit=True):
        obj = super(FormFlatPageTranslation, self).save(commit=False)

        obj.content_object = self.cleaned_data['flatpage']

        if commit:
            obj.save()

        return obj

class AdminFlatPageTranslation(ModelAdmin):
    form = FormFlatPageTranslation

try:
    admin.site.register(FlatPageTranslation, AdminFlatPageTranslation)
except AlreadyRegistered:
    pass

