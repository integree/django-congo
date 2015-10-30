from appconf import AppConf
from django.conf import settings as _settings
from django.core.cache import DEFAULT_CACHE_ALIAS
import os

settings = _settings

class CongoAppConf(AppConf):
    # sites

    SITE_MODEL = None # eg. maintenance.Site

    # logs

    LOG_MODEL = None # eg. maintenance.Log
    LOG_ROOT = os.path.join(settings.BASE_DIR, 'logs')
    COMMON_ERRORS_IGNORE_LIST = []

    # cron

    CRON_MODEL = None # eg. maintenance.Cron
    JOBS_MODULE = None # eg. maintenance.jobs
    JOB_CHOICE_PATH = None # eg. os.path.join(BASE_DIR, *JOBS_MODULE.split('.'))

    # url redirects

    URL_REDIRECT_MODEL = None # eg. maintenance.UrlRedirect

    # cache

    TEMPLATE_CACHE_BACKEND = DEFAULT_CACHE_ALIAS # eg. template_cache

    # admin

    ADMIN_MODEL = 'congo.utils.admin.ModelAdmin'
    ADMIN_PATH = '/admin/'
    ADMIN_LANGUAGE_CODE = settings.LANGUAGE_CODE
