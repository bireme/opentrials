#!/usr/bin/env python

from urllib import urlopen
import re

BASE = 'http://www.ensaiosclinicos.gov.br/rg/?page='

re_link = re.compile(
    r'''<a href="http://www\.ensaiosclinicos\.gov\.br/rg/(RBR-.*?)/">\1</a>''')

re_current = re.compile(r'''<span class="current">\s*(\d+)\s*</span>''')

page = 1
html_ant = ''

trial_ids = []
while True:
    #print '*' * 50, page
    html = urlopen(BASE+str(page)).read()
    res = re_current.findall(html)
    if len(res) == 0:
        break
    assert len(res) == 1
    assert int(res[0]) == page
    res = re_link.findall(html)
    trial_ids.extend(res)
    page += 1
for t in trial_ids:
    print t


# em 2011-12-14 este script, bem como a inpeção visual da lista pública de 
# ensaios, revela 53 ensaios publicados, porém o scoreboard na página
# principal do site diz "There are 59 registered trials."

