from django.utils.cache import patch_vary_headers
from django.utils import translation

class UserLocaleMiddleware(object):
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context. This allows pages to be dynamically
    translated to the language the user desires (if the language
    is available, of course).
    """

    def process_request(self, request):
        if request.user.is_authenticated():
            language = request.user.get_profile().preferred_language
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
        else:
            language = translation.get_language_from_request(request)
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
