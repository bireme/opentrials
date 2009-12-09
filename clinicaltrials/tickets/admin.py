# -*- coding: utf-8 -*-

from django.contrib import admin
from clinicaltrials.tickets.models import *

class TicketAdmin(admin.ModelAdmin):
    list_display = ('date_registration','subject','status',)

admin.site.register(Ticket, TicketAdmin)