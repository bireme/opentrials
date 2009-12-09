# -*- coding: utf-8 -*-

from django.contrib import admin
from clinicaltrials.tickets.models import *

class TicketAdmin(admin.ModelAdmin):
    list_display = ('created','context',)
    list_display_links = ('context',)
    search_fields = ('context',)

    def save_model(self, request, instance, form, change):
        instance.creator = request.user
        super(TicketAdmin, self).save_model(request, instance, form, change)

class FollowupAdmin(admin.ModelAdmin):
    list_display = ('date_iteration','subject','status',)
        
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Followup, FollowupAdmin)