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
    template = '''
    <h1>settings path</h1>
    <pre>%(settingspath)s</pre>
    <h1>svn info</h1>
    <pre>%(svninfo)s</pre>
    <h1>sys.path</h1>
    <pre>%(syspath)s</pre>
    '''
    import sys
    import settings
    from subprocess import Popen, PIPE
    svnout, svnerr = Popen(['svn', 'info', settings.PROJECT_PATH], stdout=PIPE).communicate()
    return HttpResponse(template % {'settingspath': settings.PROJECT_PATH,
                                    'syspath':'\n'.join(sys.path),
                                    'svninfo':svnout or svnerr})

@user_passes_test(lambda u: u.is_staff)
def raise_error(request):
    class FakeError(StandardError):
        ''' this is just to test error e-mails and logging '''
    raise FakeError('This is not really an error')



