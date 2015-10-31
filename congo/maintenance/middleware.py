# -*- coding: utf-8 -*-
from congo.conf import settings
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.http.response import Http404, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils import translation

class SiteMiddleware(object):
    def process_request(self, request):
        is_admin_backend = getattr(request, 'is_admin_backend', False)

        model_name = settings.CONGO_SITE_MODEL
        if not model_name:
            raise ImproperlyConfigured("In order to use Site model, configure settings.CONGO_SITE_MODEL first.")
        model = apps.get_model(*model_name.split('.', 1))

        try:
            site = model.objects.get_by_request(request)
            settings.SITE_ID = site.id
            request.site = site

            if not site.is_active and not is_admin_backend:
                raise Http404("Site not active for domain %s" % site.domain)

        except model.DoesNotExist:
            if settings.DEBUG:
                site = model.objects.get_by_id(settings.SITE_ID)
                request.site = site
            else:
                raise Http404("Site not found for domain %s" % request.get_host())

class SiteLanguageMiddleware(object):
    def process_request(self, request):
        is_admin_backend = getattr(request, 'is_admin_backend', False)

        site = getattr(request, 'site')
        if site:
            if is_admin_backend:
                language = settings.CONGO_ADMIN_LANGUAGE_CODE
            else:
                language = site.language
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()

class UrlRedirectMiddleware(object):
    def process_response(self, request, response):
        model_name = settings.CONGO_URL_REDIRECT_MODEL
        if not model_name:
            raise ImproperlyConfigured("In order to use UrlRedirect model, configure settings.CONGO_URL_REDIRECT_MODEL first.")
        model = apps.get_model(*model_name.split('.', 1))

        if response.status_code == 404:
            redirect_url, is_permanent_redirect = model.get_redirect_tuple(request.get_full_path())
            if redirect_url:
                if is_permanent_redirect:
                    return HttpResponsePermanentRedirect(redirect_url)
                else:
                    return HttpResponseRedirect(redirect_url)

        return response
