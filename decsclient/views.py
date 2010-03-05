from django.http import HttpResponse

from xml.etree.ElementTree import ElementTree
import urllib

DECS_SERVICE = 'http://decs.bvs.br/cgi-bin/mx/cgi=@vmx/decs'
JSON_TERM = '{"fields":{"description":"%s","label":"%s"}}'

def getterm(request, lang, code):
    params = urllib.urlencode({
        'tree_id': code or '',
        'lang': lang,
        })
    resource = urllib.urlopen(DECS_SERVICE, params)

    tree = ElementTree()
    tree.parse(resource)

    result = tree.find("decsws_response/tree/self/term_list/term")
    if result is None:
        lists = tree.findall('decsws_response/tree/term_list')
        term_list = [l for l in lists if l.attrib['lang'] == lang].pop()
        result = term_list.getiterator('term')

        json = '[%s]' % ','.join((JSON_TERM % (r.text,r.attrib['tree_id']) for r in result))
    else:
        json = '[%s]' % (JSON_TERM % (result.text,result.attrib['tree_id']))
           
    return HttpResponse(json, mimetype='application/json');

def search(request, lang, term):
    params = urllib.urlencode({
        'words': term,
        'lang': lang,
        })
    resource = urllib.urlopen(DECS_SERVICE, params)

    tree = ElementTree()
    tree.parse(resource)

    result = tree.findall('decsws_response/tree/self/term_list/term')

    json = '[%s]' % ','.join((JSON_TERM % (t.text,t.attrib['tree_id']) for t in result))
    return HttpResponse(json, mimetype='application/json');