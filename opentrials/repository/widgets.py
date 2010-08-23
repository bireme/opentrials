from django import forms
from django.forms.util import flatatt
from django.utils.safestring import mark_safe

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
