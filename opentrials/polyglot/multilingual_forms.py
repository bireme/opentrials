from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import EMPTY_VALUES
from django.forms.models import BaseModelFormSet
from django.utils.translation import ugettext_lazy as _
from django.forms.models import modelformset_factory as django_modelformset_factory

from models import Translation, get_multilingual_fields
import re

# --------- WIDGETS --------

class BaseMultilingualWidget(forms.Widget):
#    class Media:
#        js = (settings.MEDIA_URL + 'js/multilingual.js',)
#        css = {'screen': (settings.MEDIA_URL + 'css/multilingual.css',)}

    instance = None
    available_languages = ('en',)
    default_second_language = None
    widget_class = forms.TextInput
    form_data = None

    def __init__(self, widget_class, attrs=None):
        self.widget_class = widget_class
        super(BaseMultilingualWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        # Calculates values
        values = {}

        for lang in self.available_languages:
            # fixme: get from settings # English is the default language
            if lang == 'en':
                values[lang] = value

            # If there is initial value for this field
            elif self.form_data:
                values[lang] = self.form_data['%s|%s'%(name,lang)]

            # If there is an instance (modifying), get translation from it
            elif self.instance:
                values[lang] = value
                try:
                    # try to remove the formset prefix
                    column = name
                    pattern = re.compile('^[a-z_][a-z0-9_]*-[0-9]+-(.+)$')
                    match = pattern.match(column)
                    if match:
                        column = match.group(1)
                        
                    # Just get translation translation helper object for given language
                    translation = self.instance.translations.get(language=lang)
                    values[lang] = getattr(translation, column, '')
                except self.instance.translations.model.DoesNotExist:
                    values[lang] = ''

            # If it's adding, translated value is empty
            else:
                values[lang] = ''

        # Creates and renders widgets
        wargs = self.get_widget_args()
        widgets, rendereds = [], []
        for lang,label in settings.MANAGED_LANGUAGES_CHOICES:
            lang = lang.lower()
            widget = self.widget_class(**wargs)
            widgets.append(widget)
            # FIXME: get main language from settings
            w_name = lang == 'en' and name or '%s|%s'%(name,lang)

            css_class = 'multilingual-value '+lang
            if lang == self.default_second_language:
                css_class = ' '.join([css_class, 'default-second-language'])

            rendereds.append('<div class="%s"><b>%s</b>%s</div>' % (css_class, label, widget.render(w_name, values[lang])))
        # FIXME: change multilingual to polyglot
        return '<div class="multilingual">%s</div>'%('\n'.join(rendereds))

    def get_widget_args(self):
        return {}

    #def value_from_datadict(self, data, files, name):
    #    raise Exception(super(BaseMultilingualWidget, self).value_from_datadict(data, files, name))

class MultilingualTextInput(BaseMultilingualWidget):
    def __init__(self, *args, **kwargs):
        super(MultilingualTextInput, self).__init__(widget_class=forms.TextInput, *args, **kwargs)

    #def get_widget_args(self):
    #    raise Exception(self.attrs)
    #    return {'max_length': self.max_length}

class MultilingualTextarea(BaseMultilingualWidget):
    def __init__(self, *args, **kwargs):
        super(MultilingualTextarea, self).__init__(widget_class=forms.Textarea, *args, **kwargs)

class BaseMultilingualSelect(object):
    display_language = 'en' # FIXME: shouldn't be settings.LANGUAGE_CODE?
    instance = None
    model = None
    label_field = None

    def get_translated_choices(self):
        choices = []

        # Loops in the model choice objects
        for item in self.model.objects.all():
            # If there is a translation...
            try:
                item_trans = item.translations.get(language__iexact=self.display_language)
            # If there is no translation (so the original object is returned)
            except ObjectDoesNotExist:
                item_trans = item

            choices.append((item.pk, getattr(item_trans, self.label_field)))

        return choices

class MultilingualSelect(forms.Select, BaseMultilingualSelect):
    def __init__(self, display_language=None, model=None, label_field=None, attrs=None):
        self.display_language = display_language or self.display_language
        self.model = model
        self.label_field = label_field

        super(MultilingualSelect, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        self.choices = self.get_translated_choices()

        return super(MultilingualSelect, self).render(name, value, attrs)

class MultilingualSelectMultiple(forms.SelectMultiple, BaseMultilingualSelect):
    def __init__(self, display_language=None, model=None, label_field=None, attrs=None):
        self.display_language = display_language or self.display_language
        self.model = model
        self.label_field = label_field

        super(MultilingualSelectMultiple, self).__init__(attrs)

    def render(self, name, value, attrs=None, choices=()):
        self.choices = self.get_translated_choices()

        return super(MultilingualSelectMultiple, self).render(name, value, attrs, choices)

# FIELDS

class MultilingualField(forms.Field):
    """Used in replacement to CharField and Field w/ Textarea on multilingual fields"""

    instance = None
    #FIXME: get main language from settings
    available_languages = ('en',)
    default_second_language = None

class MultilingualCharField(MultilingualField):
    widget = MultilingualTextInput

    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        super(MultilingualCharField, self).__init__(*args, **kwargs)

class MultilingualTextField(MultilingualField):
    widget = MultilingualTextarea

class MultilingualModelChoiceField(MultilingualField):
    widget = MultilingualSelect
    model = None
    label_field = None

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.label_field = kwargs.pop('label_field')

        super(MultilingualModelChoiceField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return None
        try:
            value = self.model.objects.get(pk=value)
        except ObjectDoesNotExist:
            raise ValidationError(self.error_messages['invalid_choice'])
        return value

class MultilingualModelMultipleChoiceField(MultilingualModelChoiceField):
    widget = MultilingualSelectMultiple

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return None

        return self.model.objects.filter(pk__in=value)

# ---------- FORMS -----------

class MultilingualBaseForm(forms.ModelForm):
    available_languages = [code.lower() for code in settings.MANAGED_LANGUAGES]
    default_second_language = 'pt-br' # FIXME: shouldn't be settings.LANGUAGE_CODE?
    display_language = 'pt-br' # FIXME: shouldn't be settings.LANGUAGE_CODE?

    def __init__(self, *args, **kwargs):
        # Gets multilingual fields from translation class
        self.multilingual_fields = get_multilingual_fields(self._meta.model)

        if self.multilingual_fields:
            # Gets default second language from arguments, if informed. Default value is None
            self.default_second_language = kwargs.pop('default_second_language', self.default_second_language) # Optional
            self.available_languages = kwargs.pop('available_languages', [code.lower() for code in settings.MANAGED_LANGUAGES]) # Mandatory (FIXME, to remove default tuple)
            self.display_language = kwargs.pop('display_language', self.display_language)

            # Change field widgets replacing common TextInput and Textarea to Multilingual respective ones
            for field_name in self.multilingual_fields:
                if field_name not in self.base_fields:
                    continue

                if isinstance(self.base_fields[field_name], forms.CharField):
                    if isinstance(self.base_fields[field_name].widget,forms.Textarea):
                        self.base_fields[field_name] = MultilingualTextField(
                                                            label=_(self.base_fields[field_name].label),
                                                            required=self.base_fields[field_name].required)
                    else:
                        self.base_fields[field_name] = MultilingualCharField(
                                                            label=_(self.base_fields[field_name].label),
                                                            required=self.base_fields[field_name].required,
                                                            max_length=self.base_fields[field_name].max_length)

        super(MultilingualBaseForm, self).__init__(*args, **kwargs)

        if self.multilingual_fields:
            # Sets instance attributes on multilingual fields
            for field_name in (self.multilingual_fields or []):
                if field_name not in self.fields:
                    continue

                # Field
                self.fields[field_name].instance = self.instance
                self.fields[field_name].default_second_language = self.default_second_language
                self.fields[field_name].available_languages = self.available_languages

                # Widget
                self.fields[field_name].widget.instance = self.instance
                self.fields[field_name].widget.default_second_language = self.default_second_language
                self.fields[field_name].widget.available_languages = self.available_languages

                if self.data:
                    self.fields[field_name].widget.form_data = self.data

        # Display language for multilingual select widgets
        # OBS: those aren't multilingual fields from self.multilingual_fields because their
        # translation is from another model class
        for field_name in self.fields.keys():
            if isinstance(self.fields[field_name], (MultilingualModelChoiceField,)):
                self.fields[field_name].widget.display_language = self.display_language
                self.fields[field_name].widget.model = self.fields[field_name].model
                self.fields[field_name].widget.label_field = self.fields[field_name].label_field

    def save(self, commit=True):
        obj = super(MultilingualBaseForm, self).save(commit=commit)

        if commit:
            self.save_translations(obj)
            # to check fields after the update of the translations --- strange code TODO: check it
            obj = super(MultilingualBaseForm, self).save(commit=commit)
        
        return obj

    def save_translations(self, obj):
        """This method is because you can save without commit, so you can call this yourself."""

        if not hasattr(obj, 'translations'):
            return
        
        for lang,label in settings.TARGET_LANGUAGES:
            lang = lang.lower()
            # Get or create translation object
            try:
                trans = obj.translations.get(language=lang)
            except obj.translations.model.DoesNotExist:
                trans = obj.translations.model(language=lang)
                trans.content_object = obj

            # Sets fields values
            for field_name in (self.multilingual_fields or []):
                # FIXME: get main language from settings
                if lang == 'en' or field_name not in self.fields:
                    continue

                field_name_trans = '%s|%s'%(field_name,lang)
                if self.prefix:
                    field_name_trans = '%s-%s'%(self.prefix,field_name_trans)

                if field_name_trans in self.data:
                    setattr(trans, field_name, self.data[field_name_trans])

            trans.save()

class MultilingualBaseFormSet(BaseModelFormSet):
    """Fixing the bug registered at: http://code.djangoproject.com/ticket/10284"""

    display_language = 'en' # FIXME: shouldn't be settings.LANGUAGE_CODE?
    available_languages = ('en',)
    default_second_language = None

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 queryset=None, **kwargs):
        self.queryset = queryset
        defaults = {'data': data, 'files': files, 'auto_id': auto_id, 'prefix': prefix}
        defaults.update(kwargs)
   
        self.available_languages = kwargs.pop('available_languages', [code.lower() for code in settings.MANAGED_LANGUAGES]) # Mandatory (FIXME, to remove default tuple)
        self.default_second_language = kwargs.pop('default_second_language', self.default_second_language)
        self.display_language = kwargs.pop('display_language', self.display_language)

        super(BaseModelFormSet, self).__init__(**defaults)

    # Override
    def save(self, commit=True):
        if not commit:
            self.saved_forms = []
            def save_m2m():
                for form in self.saved_forms:
                    form.save_m2m()
            self.save_m2m = save_m2m

        saved_instances = self.save_existing_objects(commit) + self.save_new_objects(commit)

        if commit:
            for form in self.forms:
                if form.is_valid() and form.instance.pk:
                    form.save_translations(form.instance)

        return saved_instances

    # Override
    def save_existing_objects(self, commit=True):
        self.changed_objects = []
        self.deleted_objects = []
        if not self.get_queryset():
            return []

        saved_instances = []
        for form in self.initial_forms:
            pk_name = self._pk_field.name
            raw_pk_value = form._raw_value(pk_name)
            
            pk_value = form.fields[pk_name].clean(raw_pk_value)
            pk_value = getattr(pk_value, 'pk', pk_value)

            obj = self._existing_object(pk_value)
            if self.can_delete:
                raw_delete_value = form._raw_value(DELETION_FIELD_NAME)
                should_delete = form.fields[DELETION_FIELD_NAME].clean(raw_delete_value)
                if should_delete:
                    self.deleted_objects.append(obj)

                    # http://code.djangoproject.com/attachment/ticket/10284/modelformset_false_delete.diff
                    if commit:
                        obj.delete()
                        
                    continue
            if form.has_changed():
                self.changed_objects.append((obj, form.changed_data))
                saved_instances.append(self.save_existing(form, obj, commit=commit))
                if not commit:
                    self.saved_forms.append(form)
        return saved_instances

    def _construct_form(self, i, **kwargs):
        form = super(MultilingualBaseFormSet, self)._construct_form(i, **kwargs)

        # This override exists to set the following language-related attributes to children forms
        form.available_languages = self.available_languages
        form.default_second_language = self.default_second_language
        form.display_language = self.display_language

        return form

def modelformset_factory(*args, **kwargs):
    """This is just a monkey path to implement the argument 'extra_formset_attrs' to set extra
    attributes to formset instance"""

    # Stores extra formset attributes
    extra_formset_attrs = kwargs.pop('extra_formset_attrs', None)

    # Does what Django does
    formset_class = django_modelformset_factory(*args, **kwargs)

    # Sets attributes to formset class
    if isinstance(extra_formset_attrs, dict):
        for k,v in extra_formset_attrs.items():
            setattr(formset_class, k, v)

    return formset_class

