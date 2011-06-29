from repository.models import ClinicalTrial, ClinicalTrialTranslation
from django.template import Library, Node, TemplateSyntaxError

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
        request = context['request']

        object_list = ClinicalTrial.fossils.recruiting()
        object_list = object_list.proxies(language=request.LANGUAGE_CODE)

        """
        object_list = ClinicalTrial.published.filter(recruitment_status__label='recruiting').order_by('-date_registration',)[:self.num]
    
        for obj in object_list:
            try:
                trans = obj.translations.get(language__iexact=request.LANGUAGE_CODE)
            except ClinicalTrialTranslation.DoesNotExist:
                trans = None
            
            if trans:
                if trans.public_title:
                    obj.public_title = trans.public_title
                if trans.public_title:
                    obj.scientific_title = trans.scientific_title
        """
            
        context[self.varname] = object_list
        return ''

get_latest_recruiting_trials = register.tag(get_latest_recruiting_trials)

