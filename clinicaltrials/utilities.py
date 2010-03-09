#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse

def smoke_test(request):
    from datetime import datetime
    return HttpResponse(datetime.now().strftime('%H:%M:%S'))

def req_dump(request):
    template = '''
    <form action="./" method="POST">
    <input type="text" name="word" value="mitochondrial">
    <input type="submit" name="btn1" value="one">
    <input type="submit" name="btn2" value="two">
    </form>
    <table border="1">
       <tr><th>key</th><th>POST[key]</th></tr>
    %s
    </table>
    '''
    rows = []
    for k in request.POST.keys():
        rows.append('<tr><th>%s</th><td>%s</td></tr>' % (k, request.POST[k]))
    return HttpResponse(template % ('\n'.join(rows)))


ELLIPSIS = u'\u2026'

def safe_truncate(text, max_length=60, ellipsis=ELLIPSIS, encoding='utf-8',
                  raise_exc=False):
    u'''truncate a string without breaking words

        >>> safe_truncate(u'the time has come', 9, u'>')
        u'the time>'
        >>> safe_truncate(u'the-time-has-come', 9, u'>')
        u'the-time>'
        >>> safe_truncate(u'the time', 8)
        u'the time'
        >>> safe_truncate(u'the time', 9)
        u'the time'
        >>> s = u'uncharacteristically-long'
        >>> safe_truncate(s, 10, u'>')
        u'uncharacteristically>'
        >>> safe_truncate(s, 10, u'>', raise_exc=True)
        Traceback (most recent call last):
          ...
        ValueError: Cannot safely truncate to 10 characters
    '''
    if not isinstance(text, unicode):
        text = text.decode(encoding)
    if len(text) <= max_length:
        return text
    # reverse-seek a non-alphanumeric character
    for i, c in enumerate(reversed(text[:max_length])):
        if not c.isalnum():
            pos = max_length - i - 1
            break
    else:
        pos = -1
    if pos == -1:
        if raise_exc:
            msg = 'Cannot safely truncate to %s characters'
            raise ValueError(msg % max_length)
        else:
            # seek nearest non-alphanumeric character after the cuttoff point
            pos = len(text)
            for i, c in enumerate(text[max_length:]):
                if not c.isalnum():
                    pos = max_length + i
                    break
            if pos == len(text):
                return text

    return text[:pos] + ellipsis


if __name__=='__main__':
    import doctest
    doctest.testmod()