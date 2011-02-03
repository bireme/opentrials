from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from lxml.etree import ElementTree
import urllib
import django.utils.simplejson as json
import re

ICD10_LANGS = ['en','es','pt'] # currently only the portuguese is supported

def get_chapters(request):
    params = {}
    results = {}
    
    language = 'pt'
#    language = request.LANGUAGE_CODE.lower()
#    if language == 'pt-br':
#        language = 'pt'
    
    params = urllib.urlencode({
        'LI': 'CAPITULO',
        })

    resource = urllib.urlopen(settings.ICD10_SERVICE, params)

    tree = ElementTree()
    tree.parse(resource)

    terms = tree.findall('cid10ws_response')
    
    for term in terms:
        description = {}
        for lang in ICD10_LANGS:
            term_trans = term.findall('record_list/record/descriptor_list/descriptor[@lang="%s"]' % lang)[0]
            description[lang] = term_trans.text.strip().capitalize() if term_trans.text is not None else ""
                
        results[ term.attrib['tree_id'] ] = description

    data = []
    for id, desc in results.items():
        data.append({'fields': {"description": desc, "label": id}}) 

    data.sort(key=lambda x: x['fields']['description'][language])
        
    return HttpResponse(json.dumps(data), mimetype='application/json')

def search(request, lang, term, prefix='TV'):

    count = 30
    lang = 'pt' # currently only the portuguese is supported
    if 'count' in request.GET and request.GET['count'].isdigit():
        count = request.GET['count']

    term = term.strip()
    match = re.match('^"([^"]+)"$',term)
    if re.match('^"[^"]+"$',term):
        term = match.group(1)
        prefix = 'TZ'
    elif prefix != 'LI' and len(term.split(' ')) > 0:
        term = ' AND '.join( term.split(' ') )

    params = urllib.urlencode({
        'bool': '%s %s' % (prefix, term.encode('iso-8859-1')),
        'lang': lang,
        'count': count,
        })
        
    resource = urllib.urlopen(settings.ICD10_SERVICE, params)
    
    tree = ElementTree()
    tree.parse(resource)

    occurences = tree.findall('/cid10ws_response')

    data = []
    for occ in occurences:
        descriptors = occ.findall('record_list/record/descriptor_list/descriptor')
        description = {}
        for d in descriptors:
            description[d.attrib['lang']] = d.text.replace('\n', ' ') if d.text is not None else ""

        data.append({'fields': {"description": description, "label": occ.attrib['tree_id']}})

    data.sort(key=lambda x: x['fields']['description'][lang])
    
    return HttpResponse(json.dumps(data), mimetype='application/json')

def test_search(request):
    return render_to_response("icd10client/test_search.html", request)

