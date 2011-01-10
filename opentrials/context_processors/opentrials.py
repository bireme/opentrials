from django.conf import settings
from django.core.cache import cache
import urllib
from django.utils.safestring import mark_safe

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
    
def latest_tweets(request):
    if not settings.TWITTER:
        return {"tweets": ""}
    
    tweets = cache.get('tweets', '')
    
    if tweets:
        return {"tweets": tweets}

    tweets = urllib.urlopen("http://twitter.com/statuses/user_timeline/"+ settings.TWITTER +".json?callback=twitterCallback2&count=1").readlines()
    if len(tweets) > 0:
        tweets = mark_safe(tweets[0])
        cache.set('tweets', tweets, settings.TWITTER_TIMEOUT)

    return {"tweets": tweets}

def debug(request):
    return {'DEBUG': settings.DEBUG}
    
def default_from_email(request):
    return {'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL}

