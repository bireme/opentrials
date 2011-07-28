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
                message = MailMessage.objects.get(label='outdated').description
                if '%s' in message:
                    message = message % ct.public_title
                send_opentrials_email(subject, message, ct.submission.creator.email)

            outdated = self.is_outdate(ct, 15) #15 days of tolerance

            if outdated != ct.outdated:
                ct.outdated = outdated
                ct.save(dont_update=True)
            
            if ct.recruitment_status and ct.recruitment_status.id == 2 and ct.enrollment_end_actual is not None:
                t_delta = datetime.today() - datetime.strptime(ct.enrollment_end_actual, "%Y-%m-%d")
                if t_delta > 0 and not t_delta.days % 180:
                    subject = "Trial enrollment date checker"
                    message = MailMessage.objects.get(label='enrollment_end').description
                    if '%s' in message:
                        message = message % ct.public_title
                    send_opentrials_email(subject, message, ct.submission.creator.email)

    def handle(self, **kwargs):
        self.job()


