from django.contrib.syndication.feeds import Feed
from django.utils.translation import ugettext_lazy as _
from repository.models import ClinicalTrial

class LastTrials(Feed):
    title = _('Last published trials')
    link = '/'

    def items(self):
        return ClinicalTrial.published.all()

    def item_link(self, trial):
        return '/rg/%s/'%trial.trial_id

class LastRecruiting(Feed):
    title = _('Last published trials')
    link = '/'

    def items(self):
        return ClinicalTrial.fossils.recruiting()
        
    def item_link(self, trial):
        return '/rg/%s/'%trial.trial_id
