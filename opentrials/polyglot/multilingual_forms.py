from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import EMPTY_VALUES

from models import Translation
import re
# WIDGETS

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

