# -*- coding: utf-8 -*-
from datetime import datetime
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.datastructures import SortedDict
from django.utils.encoding import force_text
from django.views.debug import get_exception_reporter_filter
import logging
import os
from unidecode import unidecode

class BaseHandler(logging.Handler):
    def get_request_repr(self, record):
        try:
            request = record.request
            exception_reporter_filter = get_exception_reporter_filter(request)
            request_repr = force_text(exception_reporter_filter.get_request_repr(request))
        except Exception, e:
            request_repr = None
        return request_repr

    def get_user(self, record, default = 'AnonymousUser'):
        if hasattr(record, 'user'):
            user = record.user
        elif hasattr(record, 'request') and hasattr(record.request, 'user'):
            user = record.request.user
        else:
            user = None
        return unicode(user) if user else unicode(default)

    def get_extra_info(self, record):
        if hasattr(record, 'extra_info'):
            if type(record.extra_info) in (tuple, list):
                extra_info = "\n".join([unicode(obj) for obj in record.extra_info])
            elif type(record.extra_info) in (dict, SortedDict):
                extra_info = ""
                if 'list' in record.extra_info:
                    extra_info = "\n".join(record.extra_info.pop('list')) + "\n\n"
                extra_info += "\n".join(["%s: %s" % (key, val) for key, val in record.extra_info.iteritems()])
            else:
                extra_info = unicode(record.extra_info)
        else:
            extra_info = None
        return extra_info

    def get_name(self, record):
        return u"[%s] %s" % (record.levelname, record.getMessage())

    def get_message(self, record):
        self.format(record)
        exc_text = getattr(record, 'exc_text', None)
        extra_info = self.get_extra_info(record)
        request_repr = self.get_request_repr(record)

        return "\n\n".join([unidecode(text) for text in [exc_text, extra_info, request_repr] if text]) or ""

class ConsoleHandler(BaseHandler):
    def emit(self, record):
        line = "\n%s\n" % ("#" * 72)

        print line
        print self.get_name(record)
        print u"User: %s" % self.get_user(record)
        print u"Time: %s" % str(datetime.now())
        print ""
        print self.get_message(record)
        print line

class FileHandler(BaseHandler):
    def emit(self, record):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%Y-%m-%d %H:%M:%S")

        filename = "%s.txt" % date
        file_path = os.path.join(settings.CONGO_LOG_ROOT, filename)

        header = u"### %s \n%s (%s)\n\n" % (time, self.get_name(record), self.get_user(record))
        content = u"%s\n\n" % self.get_message(record)

        try:
            f = open(file_path, 'a')
            f.write(header.encode('utf8'))
            f.write(content.encode('utf8'))
            f.close()
        except:
            pass

class DataBaseHandler(BaseHandler):
    def emit(self, record):
        model_name = settings.CONGO_LOG_MODEL
        if not model_name:
            raise ImproperlyConfigured("In order to use Log model, configure settings.CONGO_LOG_MODEL first.")
        model = apps.get_model(*model_name.split('.', 1))

        try:
            log = model(name = record.name, level = record.levelno, user = self.get_user(record), message = record.getMessage(), args = self.get_message(record))
            log.save()
        except:
            pass
