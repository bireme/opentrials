from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

def smoke_test(request):
    from datetime import datetime
    return HttpResponse(datetime.now().strftime('%H:%M:%S'))

@user_passes_test(lambda u: u.is_staff)
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
    <hr>
    <p>
      <a href="this_is_a_broken_link">Click to test broken link notification</a>
    </p>
    '''
    rows = []
    for k in request.POST.keys():
        rows.append('<tr><th>%s</th><td>%s</td></tr>' % (k, request.POST[k]))
    return HttpResponse(template % ('\n'.join(rows)))

@user_passes_test(lambda u: u.is_staff)
def sys_info(request):
    template = u'''
    <h1>Site.objects.get_current()</h1>
    <table border="1">
       <tr><th>id</th><td>%(site.pk)r</td></tr>
       <tr><th>domain</th><td>%(site.domain)r</td></tr>
       <tr><th>name</th><td>%(site.name)r</td></tr>
    </table>
    <h1>settings path</h1>
    <pre>%(settingspath)s</pre>
    <h1>svn info</h1>
    <pre>%(svninfo)s</pre>
    <h1>sys.path</h1>
    <pre>%(syspath)s</pre>
    '''
    import sys
    import settings
    from django.contrib.sites.models import Site
    from subprocess import Popen, PIPE
    site = Site.objects.get_current()
    svnout, svnerr = Popen(['svn', 'info', settings.PROJECT_PATH], stdout=PIPE).communicate()
    return HttpResponse(template % {'site.pk':site.pk,
                                    'site.domain':site.domain,
                                    'site.name':site.name,
                                    'settingspath': settings.PROJECT_PATH,
                                    'syspath':'\n'.join(sys.path),
                                    'svninfo':svnout.decode('utf-8') or svnerr.decode('utf-8')})

@user_passes_test(lambda u: u.is_staff)
def raise_error(request):
    class FakeError(StandardError):
        ''' this is just to test error e-mails and logging '''
    raise FakeError('This is not really an error')



