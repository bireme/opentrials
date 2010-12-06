from django import forms
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.dates import MONTHS

from datetime import date

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
        
class YearMonthWidget(forms.MultiWidget):
    """
    This widget shows two combos with year and month and returns as a date of first day
    of that month
    """

    def __init__(self, *args, **kwargs):
        MONTHS_CHOICES = [('','-------')] + MONTHS.items()
        year = date.today().year
        YEARS_CHOICES = [('','-------')] + [(y,y) for y in range(year-1, year+50)]
        widgets = [
                forms.Select(choices=MONTHS_CHOICES),
                forms.Select(choices=YEARS_CHOICES),
                ]

        super(YearMonthWidget, self).__init__(widgets=widgets, *args, **kwargs)

    def decompress(self, value):
        if not value:
            ret = ['', '']
        else:
            ret = map(int, value.split('-')[:2])
            ret.reverse()
        return ret

    def value_from_datadict(self, data, files, name):
        month, year = data[name+'_0'], data[name+'_1']

        try:
            return date(int(year), int(month), 1)
        except ValueError:
            return None

