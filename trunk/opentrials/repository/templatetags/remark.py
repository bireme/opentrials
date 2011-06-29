from reviewapp.models import Remark
from django.template import Library, Node

register = Library()

@register.tag
def get_remarks(parser, token):
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "get_remarks tag takes exactly three arguments"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to the get_remarks tag must be 'as'"
    return RemarkList(parser.compile_filter(bits[1]), bits[3])

class RemarkList(Node):
    def __init__(self, subject, varname):
        self.subject = subject
        self.varname = varname
    
    def render(self, context):
        subject = self.subject.resolve(context,True)
        context[self.varname] = Remark.objects.filter(context=subject)
        return ''
