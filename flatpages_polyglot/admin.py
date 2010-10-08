from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AlreadyRegistered
from django import forms
from django.contrib.contenttypes.generic import GenericTabularInline as TabularInline
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin

from reversion.admin import VersionAdmin

from models import FlatPageTranslation, FlatPage

class FormFlatPageTranslation(forms.ModelForm):
    class Meta:
        model = FlatPageTranslation
        fields = ('language','title','content')

    #flatpage = forms.ModelChoiceField(queryset=FlatPage.objects.all())

    #def __init__(self, *args, **kwargs):
    #    super(FormFlatPageTranslation, self).__init__(*args, **kwargs)
    #
    #    self.fields.keyOrder = ['flatpage','language','title','content']
    #
    #    if self.instance and hasattr(self.instance.content_object, 'pk'):
    #        self.fields['flatpage'].initial = self.instance.content_object.pk

    #def save(self, commit=True):
    #    obj = super(FormFlatPageTranslation, self).save(commit=False)
    #
    #    obj.content_object = self.cleaned_data['flatpage']
    #
    #    if commit:
    #        obj.save()
    #
    #    return obj

#class AdminFlatPageTranslation(ModelAdmin):
#    form = FormFlatPageTranslation

class InlineFlatPageTranslation(TabularInline):
    model = FlatPageTranslation
    form = FormFlatPageTranslation

class NewFlatPageAdmin(VersionAdmin):
    form = FlatpageForm
    inlines = (InlineFlatPageTranslation,)
    fieldsets = FlatPageAdmin.fieldsets
    list_display = FlatPageAdmin.list_display
    list_filter = FlatPageAdmin.list_filter
    search_fields = FlatPageAdmin.search_fields

admin.site._registry[FlatPage] = NewFlatPageAdmin(FlatPage, admin.site)

#try:
#    admin.site.register(FlatPageTranslation, AdminFlatPageTranslation)
#except AlreadyRegistered:
#    pass

