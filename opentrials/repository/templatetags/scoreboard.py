from repository.models import ClinicalTrial, ClinicalTrialTranslation
from django.template import Library, Node, TemplateSyntaxError
from django.utils.translation import ugettext as _

register = Library()

def get_score_numbers(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "get_score_numbers tag takes exactly two arguments"
    if bits[1] != 'as':
        raise TemplateSyntaxError, "second argument to the get_score_numbers tag must be 'as'"

    return GetScoresNode(bits[2])

class GetScoresNode(Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        request = context['request']

        number_recruiting_trials = len(ClinicalTrial.fossils.recruiting())
        number_registered_trials = len(ClinicalTrial.fossils.published())
        scoreboard_text = "Deprecated!"

        scoreboard_result = {'number_recruiting_trials': number_recruiting_trials,
                             'number_registered_trials': number_registered_trials}

        context[self.varname] = scoreboard_result #scoreboard_text
        return ''

get_score_numbers = register.tag(get_score_numbers)
