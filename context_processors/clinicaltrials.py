import settings

def polyglot(request):
    context_extra = {}

    context_extra['MANAGED_LANGUAGES_CHOICES'] = settings.MANAGED_LANGUAGES_CHOICES
    context_extra['TARGET_LANGUAGES'] = settings.TARGET_LANGUAGES
    context_extra['MANAGED_LANGUAGES_LC'] = [c.lower() for c in settings.MANAGED_LANGUAGES]

    return context_extra