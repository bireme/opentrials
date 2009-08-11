from django.db import models

# Create your models here.

RECRUITMENT_STATUS = [
    ('pending', 'pending'),
    ('recruiting', 'recruiting'),
    ('suspended', 'suspended'),
    ('complete', 'complete'),
    ('other', 'other'),
]
 
class Registry(models.Model):
    publicTitle         = models.CharField(max_length=256, db_index=True, )
    sientificTitle      = models.CharField(max_length=256, db_index=True, )
    countryRecruitment  = models.CharField(max_length=4, db_index=True, )
    dateFirstEnrollment = models.DateField()
    targetSampleSize    = models.IntegerField()
    recruitmentStatus   = models.CharField(max_length=16, choices=RECRUITMENT_STATUS, )    