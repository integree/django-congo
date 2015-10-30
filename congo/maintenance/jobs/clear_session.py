# -*- coding: utf-8 -*-
from congo.maintenance.jobs import BaseJob
from django.contrib.sessions.models import Session
from django.utils import timezone

class Job(BaseJob):
    def __init__(self):
        super(Job, self).__init__()
        self.description = "Clear old sessions"

    def _run(self, user, *args, **kwargs):
        result = {}

        queryset = Session.objects.filter(expire_date__lt = timezone.now())
        result['count'] = queryset.count()
        queryset.delete()

        return result

