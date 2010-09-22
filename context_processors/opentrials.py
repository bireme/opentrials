import settings

def polyglot(request):
    context_extra = {}

    context_extra['MANAGED_LANGUAGES_CHOICES'] = settings.MANAGED_LANGUAGES_CHOICES
    context_extra['TARGET_LANGUAGES'] = settings.TARGET_LANGUAGES
    context_extra['MANAGED_LANGUAGES_LC'] = [c.lower() for c in settings.MANAGED_LANGUAGES]

    return context_extra
    
def jquery(request):
    context_extra = {}

    context_extra['JQUERY_URL'] = settings.JQUERY_URL
    context_extra['JQUERY_UI_URL'] = settings.JQUERY_UI_URL

    return context_extra

def google_analytics(request):
    context_extra = {}

    if hasattr(settings, 'GOOGLE_ANALYTICS_ID') and settings.GOOGLE_ANALYTICS_ID != '':
        context_extra['GOOGLE_ANALYTICS_ID'] = settings.GOOGLE_ANALYTICS_ID

    return context_extra
