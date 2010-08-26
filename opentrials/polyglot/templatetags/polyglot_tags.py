from django import template
from django.conf import settings

register = template.Library()

class JSConstantsNode(template.Node):
    def render(self, context):
        display_language = context['request'].user.get_profile().preferred_language.lower()

        ordered_languages = ([lang[0] for lang in settings.MANAGED_LANGUAGES_CHOICES if lang[0] == display_language] +
                             [lang[0] for lang in settings.MANAGED_LANGUAGES_CHOICES if lang[0] != display_language])
        ordered_languages = map(lambda s: s.lower(), map(str, ordered_languages))

        default_second_language = ordered_languages[0] == 'en' and display_language or 'en'

        return """MULTILINGUAL_FIELDS = {
                    available_languages: %s,
                    default_second_language: '%s',
                    display_language: '%s'
                  };"""%(ordered_languages, default_second_language, display_language)

def polyglot_js_constants(parser, token):
    return JSConstantsNode()

polyglot_js_constants = register.tag(polyglot_js_constants)

