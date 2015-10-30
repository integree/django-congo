# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.encoding import force_unicode, smart_str
import csv
import os

def handle_uploaded_file(file_handler, filename):
    file_path = os.path.normpath(force_unicode(smart_str(os.path.join(settings.UPLOAD_ROOT, filename))))
    with open(file_path, 'wb+') as destination:
        for chunk in file_handler.chunks():
            destination.write(chunk)
    return file_path

def unicode_csv_reader(csv_data, **kwargs):
    csv_reader = csv.reader(csv_data, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]
