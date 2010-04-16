#!/usr/bin/env python

from poplib import POP3_SSL
from email import message_from_string
from email.header import decode_header
import re

from pprint import pprint

HOST = 'pop.gmail.com'
EMAIL = 'test1@lab.tmp.br'
PASSWD = '132548'

ACTIVATE_RE = r'''http://.*/activate/([a-fA-F0-9]{40})/'''
ACTIVATE_RE = re.compile(ACTIVATE_RE)

pop = POP3_SSL(HOST)
pop.user(EMAIL)
pop.pass_(PASSWD)
numMessages = len(pop.list()[1])
for n in range(1,numMessages+1):
    res, lines, size = pop.retr(n)
    msg = message_from_string('\n'.join(lines))
    sub = msg['Subject']
    sub, encoding = decode_header(sub)[0]
    if encoding:
        sub = sub.decode(encoding)
    print n, sub
    if not msg.is_multipart():
        body = msg.get_payload(decode=True)
        res = ACTIVATE_RE.search(body)
        print res.group()

