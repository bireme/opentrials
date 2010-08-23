from django import forms
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

class SelectWithLink(forms.widgets.Select):
    def __init__(self, attrs=None, choices=(), **kwargs):
        self.text = kwargs.pop('text', 'Link')
        self.link = kwargs.pop('link', '#')
        super(SelectWithLink, self).__init__(attrs)
        
    def render(self, name, value, attrs=None, choices=()):
        if value is None: 
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append(u'</select>')
        output.append(u'<span><a href="%s" id="%s-link" style="display: inline;">%s</a></span>' % (self.link, name, self.text))
        return mark_safe(u'\n'.join(output))
        
        
class SelectInstitution(forms.widgets.Select):
    def __init__(self, attrs=None, choices=(), **kwargs):
        self.button_label = kwargs.pop('button_label', _("New Institution"))
        self.formset_prefix = kwargs.pop('formset_prefix', 'new_contact')
        self.func = "new_institution('%s')" % self.formset_prefix
        super(SelectInstitution, self).__init__(attrs)
        
    def render(self, name, value, attrs=None, choices=()):
        if value is None: 
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append(u'</select>')
        output.append(u'<span><input id="button_new_institution" onclick="%s" type="button" value="%s"/><span>' % (self.func, self.button_label))
        return mark_safe(u'\n'.join(output))
