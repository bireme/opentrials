from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from lxml.etree import ElementTree
import urllib
from json import dumps as json_dumps
from json import loads as json_loads
import re

DECS_LANGS = ['en','es','pt']
JSON_TERM = '{"fields":{"description":"%s","label":"%s"}}'
JSON_MULTILINGUAL_TERM = '{"fields":{"description":{%s},"label":"%s"}}'

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
        descriptors = tree.findall('decsws_response/record_list/record/descriptor_list/descriptor')
        description = ','.join(['"%s":"%s"'%(d.attrib['lang'],d.text) for d in descriptors])
        json = '[%s]' % (JSON_MULTILINGUAL_TERM % (description,result.attrib['tree_id']))
    
    return HttpResponse(json, mimetype='application/json')

def getdescendants(request, code):
    params = {}
    results = {}

    for lang in DECS_LANGS:
        params[lang] = urllib.urlencode({
            'tree_id': code or '',
            'lang': lang,
            })

        resource = urllib.urlopen(settings.DECS_SERVICE, params[lang])

        tree = ElementTree()
        tree.parse(resource)

        descendants = tree.findall('decsws_response/tree/descendants/term_list[@lang="%s"]/term' % lang)
        for d in descendants:
            if d.attrib['tree_id'] in results:
                results[ d.attrib['tree_id'] ] += ',"%s":"%s"' % (lang,d.text.capitalize())
            else:
                results[ d.attrib['tree_id'] ] = '"%s":"%s"' % (lang,d.text.capitalize())

    json = '[%s]' % ','.join((JSON_MULTILINGUAL_TERM % (id,desc) for desc,id in results.items()))
    json_response = json_loads(json)
    json_response.sort(key=lambda x: x['fields']['description'][lang])
        
    return HttpResponse(json_dumps(json_response), mimetype='application/json')

def search(request, lang, term, prefix='403'):
    # about the prefix: http://wiki.reddes.bvsalud.org/index.php/DeCS_services
    count = 30
    if 'count' in request.GET and request.GET['count'].isdigit():
        count = request.GET['count']

    term = term.strip()
    match = re.match('^"([^"]+)"$',term)
    if re.match('^"[^"]+"$',term):
        term = match.group(1)
        prefix = '103'
    elif len(term) > 0:
        term = ' AND '.join( term.split(' ') )


    params = urllib.urlencode({
        'bool': '%s %s' % (prefix, term.encode('iso-8859-1')),
        'lang': lang,
        'count': count,
        })
    resource = urllib.urlopen(settings.DECS_SERVICE, params)
    
    tree = ElementTree()
    tree.parse(resource)

    occurences = tree.findall('/decsws_response')

    json = []
    for occ in occurences:
        descriptors = occ.findall('record_list/record/descriptor_list/descriptor')
        description = ','.join(('"%s":"%s"'%(d.attrib['lang'],d.text) for d in descriptors ))
        json.append(JSON_MULTILINGUAL_TERM % (description,occ.attrib['tree_id']))

    json_response = json_loads('[%s]' % ','.join(json))
    json_response.sort(key=lambda x: x['fields']['description'][lang])
    
    return HttpResponse(json_dumps(json_response), mimetype='application/json')

def test_search(request):
    return render_to_response("test_search.html", request)
