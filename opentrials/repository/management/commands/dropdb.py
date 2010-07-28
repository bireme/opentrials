from django.conf import settings
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Drop and re-create the database"

    def handle_noargs(self, **options):
        import MySQLdb
        # print "Connecting..."
        db=MySQLdb.connect(host=settings.DATABASES['default']['HOST'] or "localhost",
                           user=settings.DATABASES['default']['USER'],
                           passwd=settings.DATABASES['default']['PASSWORD'],
                           port=int(settings.DATABASES['default']['PORT'] or 3306))
        cursor = db.cursor()
        print "Dropping database %s..." % settings.DATABASES['default']['NAME'],
        cursor.execute("drop database %s; create database %s;" % 
                       (settings.DATABASES['default']['NAME'], settings.DATABASES['default']['NAME']))
        print "dropped and re-created."

