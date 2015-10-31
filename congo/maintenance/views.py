# -*- coding: utf-8 -*-
from congo.conf import settings
from django import shortcuts
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured
from django.http.response import Http404
from django.apps import apps

#@permission_required()
def cron(request, cron_id):
    model_name = settings.CONGO_CRON_MODEL
    if not model_name:
        raise ImproperlyConfigured("In order to use Cron model, configure settings.CONGO_CRON_MODEL first.")
    model = apps.get_model(*model_name.split('.', 1))

    try:
        cron = model.objects.get(id = cron_id)
    except model.DoesNotExist:
        raise Http404

#    meta = MetaData(unicode(cron))
#    meta.add_breadcrumb(None, request.path)

    result = cron.run_job(request.user)

    extra_context = {
        'result': result,
    }

    return shortcuts.render(request, 'congo/maintenance/cron.html', extra_context)
