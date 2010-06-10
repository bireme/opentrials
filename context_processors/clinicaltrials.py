import settings

def polyglot(request):
    context_extra = {}

    context_extra['MANAGED_LANGUAGES'] = settings.MANAGED_LANGUAGES
    context_extra['TARGET_LANGUAGES'] = settings.TARGET_LANGUAGES
    context_extra['CHECKED_CODES'] = [c.lower() for c in settings.CHECKED_LANGUAGES]

    return context_extra