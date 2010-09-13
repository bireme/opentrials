from django.contrib.flatpages.views import render_flatpage
from django.shortcuts import get_object_or_404
from django.conf import settings

from models import FlatPage, FlatPageTranslation

class FlatPagePolyglotMiddleware(object):
    def process_request(self, request):
        """This code was partially copied from django.contrib.flatpages.views.flatpage"""

        try:
            flatpage = FlatPage.objects.get(url__exact=request.path_info, sites__id__exact=settings.SITE_ID)
        except FlatPage.DoesNotExist:
            return None

        try:
            trans = flatpage.translations.get(language__iexact=request.LANGUAGE_CODE)

            trans.registration_required = flatpage.registration_required
            trans.template_name = flatpage.template_name
        except FlatPageTranslation.DoesNotExist:
            trans = flatpage

        return render_flatpage(request, trans)
        

