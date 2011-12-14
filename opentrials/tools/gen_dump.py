from settings import INSTALLED_APPS

print 'rm -rf rebec-2011-12-13'
print 'mkdir rebec-2011-12-13'
for app in INSTALLED_APPS:
    if app.startswith('django.contrib.'):
        short_app = app.replace('django.contrib.','')
    else:
        short_app = app
    cmd = './manage.py dumpdata -n %s --indent=2 > rebec-2011-12-13/%s-2011-12-13.json'
    print cmd % (short_app, app)
