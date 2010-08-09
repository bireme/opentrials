from django.template import Library, Node
from reviewapp.models import News

register = Library()

def get_latest_news(parser, token):
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "get_latest_news tag takes exactly three arguments"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to the get_latest_news tag must be 'as'"

    return LatestNewsNode(bits[1], bits[3])

class LatestNewsNode(Node):
    def __init__(self, num, varname):
        self.num = num
        self.varname = varname
    
    def render(self, context):
        context[self.varname] = News.objects.all().order_by('-created',)[:self.num]
        return ''

get_latest_news = register.tag(get_latest_news)

