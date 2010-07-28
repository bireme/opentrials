#!/usr/bin/env bpython

from django.core.management import setup_environ
import settings
setup_environ(settings)
from repository.models import *
from reviewapp.models import *

