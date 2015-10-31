from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps
import logging
from django.contrib.auth.models import AnonymousUser

class Command(BaseCommand):
    help = 'Runs CRON jobs for given frequency'
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('frequency', nargs = 1, type = int)

    def handle(self, *args, **options):
        from congo.conf import settings

        model_name = settings.CONGO_CRON_MODEL
        if not model_name:
            raise ImproperlyConfigured("In order to use Cron model, configure settings.CONGO_CRON_MODEL first.")
        model = apps.get_model(*model_name.split('.', 1))

        frequency = options['frequency'][0]
        frequency_dict = dict(model.FREQUENCY_CHOICE)
        try:
            frequency_label = frequency_dict[frequency]
        except KeyError:
            raise CommandError('Incorrect frequency argument. Valid values are: %s' % ', '.join(frequency_dict.keys()))

        user = AnonymousUser()
        message = "Run CRON jobs command invoked for frequency %s (%s)" % (frequency, frequency_label)
        extra = {'user': user}

        logger = logging.getLogger('system.cron')
        logger.debug(message, extra = extra)

        i = j = 0

        for cron in model.objects.filter(frequency = frequency, is_active = True):
            result = cron.run_job(user)
            j += 1
            if result['success']:
                i += 1

        self.stdout.write(message)
        self.stdout.write("Invoked: %s, completed: %s" % (i, j))
