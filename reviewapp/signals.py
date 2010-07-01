def create_user_profile(sender, instance,**kwargs):
    from reviewapp.models import UserProfile
    UserProfile.objects.get_or_create(user=instance)

def check_trial_fields(sender, instance,**kwargs):
    """
        {
            'en':{
                    'step_1': 'MISSING',
                    'step_2': 'MISSING',
                    'step_3': 'MISSING',
                    'step_4': 'MISSING',
                    'step_5': 'MISSING',
                    'step_6': 'MISSING',
                    'step_7': 'MISSING',
                    'step_8': 'MISSING',
                    'step_9': 'MISSING',
                },
        }
    """
    from repository.trds_forms import STEP_FORM_MATRIX
    from repository.models import ClinicalTrial
    import re

    for step,forms in STEP_FORM_MATRIX.items():
        for form in forms:
            if hasattr(form.Meta,'queryset'):
                count = form.Meta.queryset.filter(trial=instance).count()
                if count == 0:
                    print "MISSING %s" % form
                
            elif hasattr(form.Meta,'model'):
                if(form.Meta.model == ClinicalTrial ):
                    for field in form.declared_fields.keys():
                        value = getattr(instance,field)

                        if value is None:
                            print "MISSING %s" % field
                        elif type(value) is str or type(value) is unicode:
                            if re.match('^\s*$', value):
                                print "MISSING %s" % field
                            else:
                                print type(value)
                        else:
                            print type(value)