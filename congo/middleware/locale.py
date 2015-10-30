# -*- coding: utf-8 -*-
from congo.conf import settings
from django.core.urlresolvers import get_resolver, LocaleRegexURLResolver, resolve, reverse, Resolver404, NoReverseMatch
from django.http.response import HttpResponseRedirect
from django.utils import translation
from django.utils.http import is_safe_url
from django.utils.translation import check_for_language
from urlparse import urlparse

class LanguageMiddleware(object):
    def __init__(self):
        self._is_language_prefix_patterns_used = False
        for url_pattern in get_resolver(None).url_patterns:
            if isinstance(url_pattern, LocaleRegexURLResolver):
                self._is_language_prefix_patterns_used = True
                break

    def process_request(self, request):
        is_admin_backend = getattr(request, 'is_admin_backend', False)

        if is_admin_backend:
            language = settings.CONGO_ADMIN_LANGUAGE_CODE
        else:
            check_path = self.is_language_prefix_patterns_used()
            language = translation.get_language_from_request(request, check_path = check_path)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        if request.method == 'POST':
            language = request.POST.get('language')
            action = request.POST.get('action')
            if action == 'set_language' and check_for_language(language):
                host = request.get_host()
                next_url = request.GET.get('next', None)
                referer = request.META.get('HTTP_REFERER', None)

                if next_url:
                    if is_safe_url(url = next_url, host = host):
                        response = HttpResponseRedirect(next_url)
                elif referer:
                    if is_safe_url(url = referer, host = host):
                        referer_url = urlparse(referer)[2]
                        try:
                            # http://wenda.soso.io/questions/275666/django-templates-get-current-url-in-another-language
                            view = resolve(referer_url)
                            with translation.override(language):
                                next_url = reverse(view.view_name, args = view.args, kwargs = view.kwargs)
                                response = HttpResponseRedirect(next_url)
                        except (Resolver404, NoReverseMatch):
                            pass

                if hasattr(request, 'session'):
                    request.session[translation.LANGUAGE_SESSION_KEY] = language
                else:
                    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language, max_age = settings.LANGUAGE_COOKIE_AGE, path = settings.LANGUAGE_COOKIE_PATH, domain = settings.LANGUAGE_COOKIE_DOMAIN)

        return response

    def is_language_prefix_patterns_used(self):
        """
        Returns `True` if the `LocaleRegexURLResolver` is used
        at root level of the urlpatterns, else it returns `False`.
        """
        return self._is_language_prefix_patterns_used
