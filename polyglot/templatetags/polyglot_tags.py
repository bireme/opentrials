from django import template

from polyglot.models import get_ordered_languages

register = template.Library()

class JSConstantsNode(template.Node):
    def render(self, context):
        # It depends on 'request' template context processor
        display_language = context['request'].user.get_profile().preferred_language.lower()

        ordered_languages = get_ordered_languages(display_language, lower=True)
        
        # Default second language must be english
        if len(ordered_languages) <= 1:
            default_second_language = None
        else:
            default_second_language = ordered_languages[1]

        return """MULTILINGUAL_FIELDS = {
                    available_languages: %s,
                    default_second_language: '%s',
                    display_language: '%s'
                  };"""%(ordered_languages, default_second_language, display_language)

def polyglot_js_constants(parser, token):
    return JSConstantsNode()

polyglot_js_constants = register.tag(polyglot_js_constants)

