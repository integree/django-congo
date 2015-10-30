# -*- coding: utf-8 -*-
import logging
from congo.conf import settings

class IgnoreCommonErrors(logging.Filter):
    def filter(self, record):
        exc_text = getattr(record, 'exc_text', None)

#        common_errors = [
#            "AttributeError: 'NoneType' object has no attribute 'get_object_by_attrs'",
#            "ZeroDivisionError: integer division or modulo by zero",
#            "TypeError: argument of type 'NoneType' is not iterable",
#        ]

        common_errors = settings.CONGO_COMMON_ERRORS_IGNORE_LIST

        for e in common_errors:
            if e in exc_text:
                return False

        return True
