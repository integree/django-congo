# -*- coding: utf-8 -*-
from congo.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS

def cache_key_generator(key, key_prefix, version):
    site_id = getattr(settings, 'SITE_ID', None)
    if site_id:
        key_elemets = [str(site_id), key_prefix, str(version), key]
    else:
        key_elemets = [key_prefix, str(version), key]
    return ':'.join(key_elemets)

def template_cache_backend():
    cache_backend = settings.CONGO_TEMPLATE_CACHE_BACKEND
    if cache_backend is None:
        cache_backend = DEFAULT_CACHE_ALIAS
    return cache_backend
