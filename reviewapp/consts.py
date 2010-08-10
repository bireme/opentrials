from django.utils.translation import ugettext_lazy as _

# Form validation util constants

TRIAL_FORMS = ['Trial Identification',
               'Sponsors',
               'Health Conditions',
               'Interventions',
               'Recruitment',
               'Study Type',
               'Outcomes',
               'Contacts',
               'Attachments']

STEP_STATES = [
    (1, _('REMARK')),
    (2, _('MISSING')),
    (3, _('PARTIAL')),
    (4, _('COMPLETE'))
]

REMARK = STEP_STATES[0][0]
MISSING = STEP_STATES[1][0]
PARTIAL = STEP_STATES[2][0]
COMPLETE = STEP_STATES[3][0]

