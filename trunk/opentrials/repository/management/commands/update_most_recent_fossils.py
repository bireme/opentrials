from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.contrib.contenttypes.models import ContentType

from repository.models import ClinicalTrial
from fossil.models import Fossil

class Command(NoArgsCommand):
    help = "Delete and generate again the fossils for published Clinical Trials"

    def handle_noargs(self, **options):
        c_type = ContentType.objects.get_for_model(ClinicalTrial)
        trials = ClinicalTrial.published.all()

        # Loops published ClinicalTrials
        for trial in trials:
            # Delete most recent fossil
            Fossil.objects.filter(
                    content_type=c_type,
                    object_id=trial.pk,
                    is_most_recent=True,
                    ).delete()

            # Update clinical trial to generate fossil again
            trial.save()

