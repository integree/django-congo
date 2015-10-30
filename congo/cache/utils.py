# -*- coding: utf-8 -*-
from congo.conf import settings

def cache_key_generator(key, key_prefix, version):
    site_id = getattr(settings, 'SITE_ID', None)
    if site_id:
        key_elemets = [str(site_id), key_prefix, str(version), key]
    else:
        key_elemets = [key_prefix, str(version), key]
    return ':'.join(key_elemets)
