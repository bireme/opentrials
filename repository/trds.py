from django.utils.translation import ugettext as _

from repository.models import *

TRDS_LABELS = (
    (1,_('Primary Registry and Trial Identifying Number'), 'trial_id'),
    (2,_('Date of Registration in Primary Registry'), 'date_registration'),
    (3,_('Secondary Identifying Numbers'), 'trialnumber_set'),
    (4,_('Source(s) of Monetary or Material Support'), 'support_sources'),
    (5,_('Primary Sponsor'), 'primary_sponsor'),
    (6,_('Secondary Sponsors'), 'secondary_sponsors'),
    (7,_('Contacts for Public Queries'), 'public_contacts'),
    (8,_('Contacts for Scientific Queries'), 'scientific_contacts'),
    (9,_('Public Title'), 'public_title acronym'),
    (10,_('Scientific Title'), 'scientific_title scientific_acronym'),
    (11,_('Countries of Recruitment'), 'recruitmentcountry_set'),
)

class TRDSField(object):

    def __init__(self, trial, number, title, subfields):
        self.trial = trial
        self.number = number
        self.title = title
        self.subfields = subfields.split()

    def dump(self):
        res = []
        for attr_name in self.subfields:
            d = {'attr_name':attr_name}
            attr = getattr(self.trial, attr_name)
            if callable(attr):
                d['value'] = repr(attr())
            else:
                d['value'] = attr
            res.append(d)
        return res



'''
    # Scientific fields
    (12,_('Health Condition(s) or Problem(s) Studied')),
    (13,_('Intervention(s)')),
    (14,_('Key Inclusion and Exclusion Criteria')),
    (15,_('Study Type')),
    (16,_('Date of First Enrollment')),
    (17,_('Target Sample Size')),
    (18,_('Recruitment Status')),
    (19,_('Primary Outcome(s)')),
    (20,_('Key Secondary Outcomes')),
'''