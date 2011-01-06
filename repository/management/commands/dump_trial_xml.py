from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand

from repository.xml import generate

class Command(BaseCommand):
    help = "Dumps a string for a given function with XML for clinical trials."

    option_list = BaseCommand.option_list + (
            make_option('--function',
                dest='func',
                default='xml_opentrials',
                help="""Valid functions: %s"""%', '.join(generate.VALID_FUNCTIONS),
                ),
            )

    def handle(self, func, **options):
        try:
            func = getattr(generate, func)
        except AttributeError:
            print 'Invalid function "%s" not found in "repository.xml.generate".' % func
            print 'Valid functions are:'
            for f in generate.VALID_FUNCTIONS:
                print '\t', f
            return

        # Calls the given function with given arguments
        print func(**options)

