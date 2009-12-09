# -*- coding: utf-8 -*-

from django.contrib import admin
from clinicaltrials.tickets.models import *

class FollowupInline(admin.StackedInline):
    model = Followup

class FollowupAdmin(admin.ModelAdmin):
    list_display = ('date_iteration','subject','status',)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('created','context','creator')
    list_display_links = ('context',)
    search_fields = ('context',)
    inlines = [FollowupInline]

    def save_model(self, request, instance, form, change):
        instance.creator = request.user
        super(TicketAdmin, self).save_model(request, instance, form, change)
        
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Followup, FollowupAdmin)