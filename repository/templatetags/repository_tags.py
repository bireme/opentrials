from django import template

register = template.Library()

class ForTranslationNode(template.Node):
    def __init__(self, trans, var, nodelist):
        if '.' in trans:
            obj, self.translations = trans.split('.')
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
            obj = self.obj.resolve(context)
            for lang in languages:
                try:
                    context[self.var] = [t for t in obj['translations'] if t['language'] == lang][0]
                except IndexError:
                    context[self.var] = obj
                    obj.setdefault('language', lang)

                output.append(self.nodelist.render(context))
        else:
            translations = self.translations.resolve(context)
            for lang in languages:
                context[self.var] = [t for t in translations if t['language'].lower() == lang.lower()][0]

                output.append(self.nodelist.render(context))

        return u'\n'.join(output)

@register.tag
def for_trans(parser, token):
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
    nodelist = parser.parse(('endfor_trans',))
    parser.delete_first_token()    

    return ForTranslationNode(bits[1], bits[3], nodelist)

