from repository.models import ClinicalTrial
from django.template import Library, Node

register = Library()

def get_latest_recruiting_trials(parser, token):
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "get_latest_recruiting_trials tag takes exactly three arguments"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to the get_latest_recruiting_trials tag must be 'as'"

    return LatestRecruitingTrialsNode(bits[1], bits[3])

class LatestRecruitingTrialsNode(Node):
    def __init__(self, num, varname):
        self.num = num
        self.varname = varname
    
    def render(self, context):
        context[self.varname] = ClinicalTrial.published.filter(recruitment_status__label='recruiting').order_by('-date_registration',)[:self.num]
        return ''

get_latest_recruiting_trials = register.tag(get_latest_recruiting_trials)

