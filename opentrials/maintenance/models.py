from django.db import models
from django.contrib.auth.models import User

class MaintenanceWindow(models.Model):
    start = models.DateTimeField(auto_now_add=True, db_index=True)
    estimated_end = models.DateTimeField(null=True)
    actual_end = models.DateTimeField(null=True, blank=True, editable=False, db_index=True)
    description = models.TextField(max_length=500)
    responsible = models.ForeignKey(User, related_name='app_maintenances', editable=False)

    class Meta():
        ordering = ['-start']
        get_latest_by = 'start'

    def ended(self):
        return True if self.actual_end else False
    ended.boolean = True

    @classmethod
    def under_maintenance(cls):
        try:
            return not cls.objects.latest().ended()
        except cls.DoesNotExist:
            return False