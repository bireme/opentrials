from django.db import models
from django.forms import ModelForm


from vocabularies import COUNTRIES

class RecruitmentStatus(models.Model):
    status = models.CharField(max_length=32, db_index=True)
    label  = models.CharField(max_length=32, db_index=True)
    lang   = models.CharField(max_length=8, db_index=True)
    
    def __unicode__(self):
        return u'%s' % (self.label)
    
class RecruitmentCountry(models.Model):
    trial = models.ForeignKey('ClinicalTrial')
    country_code = models.CharField(max_length=8, choices=COUNTRIES)
    
class ClinicalTrial(models.Model):
    public_title         = models.CharField(max_length=255, db_index=True)
    scientific_title     = models.CharField(max_length=255, db_index=True)
    dateFirst_enrollment = models.DateField()
    target_sample_size   = models.IntegerField()
    recruitment_status   = models.ForeignKey('RecruitmentStatus')