from django import template
from django.template.defaultfilters import slugify

register = template.Library()

class ForTranslationNode(template.Node):
    def __init__(self, trans, var, nodelist):
        if '.' in trans:
            parts = trans.split('.')
            obj = '.'.join(parts[:-1])
            self.translations = parts[-1]
            self.obj = template.Variable(obj)
        else:
            self.obj = None
            self.translations = template.Variable(trans)
        self.var = var
        self.nodelist = nodelist

    def render(self, context):
        output = []
        languages = context['languages']

        if self.obj:
            done_languages = []
            obj = self.obj.resolve(context)

            if obj:
                for lang in languages:
                    try:
                        translations = self.get_translations(self.get_value(obj, 'translations')) or []
                        context[self.var] = [t for t in translations if self.get_value(t, 'language') == lang][0]
                    except IndexError:
                        context[self.var] = obj
                        self.set_language(obj, lang)

                    if self.get_value(context[self.var], 'language') not in done_languages:
                        output.append(self.nodelist.render(context))
                        done_languages.append(self.get_value(context[self.var], 'language'))
        else:
            translations = self.translations.resolve(context)
            for lang in languages:
                try:
                    context[self.var] = [t for t in translations if self.get_value(t, 'language').lower() == lang.lower()][0]
                except Exception, e: # FIXME
                    continue

                output.append(self.nodelist.render(context))

        return u'\n'.join(output)

    def get_value(self, obj, key):
        try:
            return obj[key]
        except TypeError:
            return None
        except KeyError:
            return None

    def get_translations(self, obj):
        return obj

    def set_language(self, obj, lang):
        obj.setdefault('language', lang)

class ForTranslationNodeObj(ForTranslationNode):
    def get_value(self, obj, key):
        return getattr(obj, key)

    def get_translations(self, obj):
        return obj.all()

    def set_language(self, obj, lang):
        obj.language = getattr(obj, 'language', lang)

#@register.tag
def do_for_trans(parser, token):
    """
    Usage example:

        {% for_trans translations as t %}
            <div class="title">
                <h2>{{ t.language }}</h2>
                <p>{{ t.scientific_title }}</p>
            </div>
        {% endfor_trans %}
    """
    bits = token.split_contents()
    nodelist = parser.parse(('end'+bits[0],))
    parser.delete_first_token()    

    if bits[0] == 'for_trans_obj':
        return ForTranslationNodeObj(bits[1], bits[3], nodelist)
    else:
        return ForTranslationNode(bits[1], bits[3], nodelist)

for_trans = register.tag('for_trans', do_for_trans)
for_trans_obj = register.tag('for_trans_obj', do_for_trans)

@register.filter
def switch(value, key_labels):
    """
    Returns the equivalent label for a given key value.
    
    The example below will return "months":

        {{ "M"|switch:"-=null,Y=years,M=months,W=weeks,D=days,H=hours" }}
    """
    key_labels = dict([item.split('=') for item in key_labels.split(',')])
    return key_labels.get(value, value)

@register.filter
def prep_label_for_xml(label):
    """Returns a label replacing whitespaces for underlines because XML validation
    doesn't support white spaces."""
    return 'null' if label == 'N/A' else slugify(label.replace(' ', '_'))

