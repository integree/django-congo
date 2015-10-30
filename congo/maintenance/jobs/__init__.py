# -*- coding: utf-8 -*-
from django.utils import timezone
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
from unidecode import unidecode
import logging
import os
import sys

class BaseJob(object):
    name = u""
    description = u""

    def __init__(self):
        self.name = self.__module__.split('.')[-1]
        self.description = u"%s job done" % self.name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return unidecode(self.name)

    def _run(self, *args, **kwargs):
        raise NotImplementedError("The _run() method should take the one user argument (User), perform a task and return result (dict or SortedDict).")

    def run(self, user, *args, **kwargs):
        logger = logging.getLogger('system.cron.%s' % self.name)

        exc_info = None
        extra = {
            'user': user,
            'extra_info': SortedDict()
        }

        start_time = timezone.now()
        try:
            result_info = self._run(user, *args, **kwargs)
            level = result_info.pop('level') if 'level' in result_info else logging.INFO
            extra['extra_info'].update(result_info)
            message = self.description or _("The job was done")
        except Exception, e:
            level = logging.ERROR
            exc_info = sys.exc_info()
            message = u"[%s] %s" % (e.__class__.__name__, e)

        end_time = timezone.now()
        extra['extra_info']['time'] = end_time - start_time

        logger.log(level, message, exc_info = exc_info, extra = extra)

        return {
            'name': self.name,
            'message': message,
            'success': level < logging.ERROR,
            'time': extra['extra_info']['time'],
        }
