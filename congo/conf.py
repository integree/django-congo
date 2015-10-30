from appconf import AppConf
from django.conf import settings as _settings
from django.core.cache import DEFAULT_CACHE_ALIAS
import os

settings = _settings

class CongoAppConf(AppConf):
    # logs

    LOG_MODEL = None
    CONGO_COMMON_ERRORS_IGNORE_LIST = []
    LOG_ROOT = os.path.join(settings.BASE_DIR, 'logs')

    # sites

    SITE_MODEL = None

    # url redirects

    URL_REDIRECT_MODEL = None

    # middleware

    ADMIN_PATH = '/admin/'
    ADMIN_LANGUAGE_CODE = settings.LANGUAGE_CODE

    # cache

    TEMPLATE_CACHE_BACKEND = DEFAULT_CACHE_ALIAS
