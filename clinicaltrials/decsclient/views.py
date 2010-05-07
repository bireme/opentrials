from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from lxml.etree import ElementTree
import urllib

JSON_TERM = '{"fields":{"description":"%s","label":"%s"}}'

def getterm(request, lang, code):
    params = urllib.urlencode({
        'tree_id': code or '',
        'lang': lang,
        })
    resource = urllib.urlopen(settings.DECS_SERVICE, params)

    tree = ElementTree()
    tree.parse(resource)

    result = tree.find("decsws_response/tree/self/term_list/term")
    if result is None:
        result = tree.findall('decsws_response/tree/term_list[@lang="%s"]/term' % lang)
        json = '[%s]' % ','.join((JSON_TERM % (r.text.capitalize(),r.attrib['tree_id']) for r in result))
    else:
        json = '[%s]' % (JSON_TERM % (result.text,result.attrib['tree_id']))
           
    return HttpResponse(json, mimetype='application/json');

def getdescendants(request, lang, code):
    params = urllib.urlencode({
        'tree_id': code or '',
        'lang': lang,
        })
    resource = urllib.urlopen(settings.DECS_SERVICE, params)

    tree = ElementTree()
    tree.parse(resource)

    result = tree.findall('decsws_response/tree/descendants/term_list[@lang="%s"]/term' % lang)
    json = '[%s]' % ','.join((JSON_TERM % (r.text.capitalize(),r.attrib['tree_id']) for r in result))

    return HttpResponse(json, mimetype='application/json');

def search(request, lang, term, prefix='401'):
    # about the prefix: http://wiki.reddes.bvsalud.org/index.php/DeCS_services
    count = 30
    if 'count' in request.GET and request.GET['count'].isdigit():
        count = request.GET['count']
        
    params = urllib.urlencode({
        'bool': '%s %s' % (prefix, term),
        'lang': lang,
        'count': count,
        })
    resource = urllib.urlopen(settings.DECS_SERVICE, params)

    tree = ElementTree()
    tree.parse(resource)

    result = tree.findall('decsws_response/tree/self/term_list/term')

    json = '[%s]' % ','.join( sorted(JSON_TERM % (t.text,t.attrib['tree_id']) for t in result) )
    return HttpResponse(json, mimetype='application/json');

def test_search(request):
    return render_to_response("test_search.html", request)