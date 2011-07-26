from repository.models import ClinicalTrial
from django.core.management import BaseCommand
from reviewapp.views import send_opentrials_email
from vocabulary.models import MailMessage
from datetime import datetime, timedelta

class Command(BaseCommand):
    
    def is_outdate(self,ct, tolerance=0):

        now = datetime.today()
        tolerance = timedelta(tolerance)

        start_planned = ct.enrollment_start_planned
        end_planned = ct.enrollment_end_planned
        start_actual = ct.enrollment_start_actual
        end_actual = ct.enrollment_end_planned

        try:
            if start_planned is not None:
                start_planned = datetime.strptime(start_planned, "%Y-%m-%d") + tolerance
                if start_planned < now and start_actual is None:
                    return True
                        
            if end_planned is not None:
                end_planned = datetime.strptime(end_planned, "%Y-%m-%d") + tolerance
                if end_planned < now and end_actual is None:
                    return True
        except ValueError:
            return True
            
        return False
                
    def job(self):
        # This will be executed each 1 day
        for ct in ClinicalTrial.objects.all():

            send_email = self.is_outdate(ct)

            if send_email:
                subject = "Trial enrollment date checker"
                message = MailMessage.objects.filter(label='outdated')[0].description
                send_opentrials_email(subject, message, ct.submission.creator.email)
            
            outdated = self.is_outdate(ct, 15)

            if outdated != ct.outdated:
                ct.outdated = outdated
                ct.save()

    
    def handle(self, **kwargs):
        self.job()


