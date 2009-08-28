from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from vocabularies import COUNTRIES

class RecruitmentStatus(models.Model):
    status = models.CharField(max_length=32, db_index=True)
    label  = models.CharField(max_length=32, db_index=True)
    lang   = models.CharField(max_length=8, db_index=True)
    
    def __unicode__(self):
        return u'%s' % (self.label)
    
    class Meta:
        verbose_name_plural = _('Recruitment status')
    
class RecruitmentCountry(models.Model):
    trial = models.ForeignKey('ClinicalTrial')
    country_code = models.CharField(max_length=8, choices=COUNTRIES)
    
class ClinicalTrial(models.Model):
    public_title         = models.CharField(_('Public Title'),
                                            max_length=255, db_index=True)
    scientific_title     = models.CharField(_('Scientific Title'),
                                            max_length=255, db_index=True)
    dt_first_enrollment  = models.DateField(_('Date of First Enrollment'))
    target_sample_size   = models.IntegerField(_('Target Sample Size'))
    recruitment_status   = models.ForeignKey('RecruitmentStatus',
                                             verbose_name=_('Recruitment Status'))