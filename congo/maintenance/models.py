# -*- coding: utf-8 -*-
from .managers import SiteManager
from congo.conf import settings
from congo.utils.managers import ActiveManager
from congo.utils.text import slugify
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from congo.maintenance import SITE_CACHE, CONFIG_CACHE

@python_2_unicode_compatible
class AbstractConfig(models.Model):
    name = models.SlugField(max_length = 255, unique = True, verbose_name = _("Name"))
    value = models.CharField(blank = True, max_length = 255, verbose_name = _("Value"))
    description = models.TextField(null = True, blank = True, verbose_name = _("Description"))
    use_cache = models.BooleanField(default = False, verbose_name = _("Use cache"))
    load_at_startup = models.BooleanField(default = False, verbose_name = _("Load at startup"))

    class Meta:
        verbose_name = _("System config")
        verbose_name_plural = _("System configs")
        ordering = ('name',)
        abstract = True

    def __str__(self):
        return self.name

    @classmethod
    def get_value(cls, name, default = None):
        global CONFIG_CACHE
        name = slugify(name)

        if name in CONFIG_CACHE:
            return CONFIG_CACHE[name]
        try:
            config = cls.objects.get(name = name)
            if config.use_cache:
                CONFIG_CACHE[name] = config.value
            return config.value
        except cls.DoesNotExist:
            return default

    @classmethod
    def set_value(cls, name, value):
        name = slugify(name)
        config, created = cls.objects.update_or_create(name = name, defaults = {'value': value})

        if config.use_cache:
            CONFIG_CACHE[name] = value

    @classmethod
    def load_cache(cls):
        global CONFIG_CACHE

        for name, value in cls.objects.filter(use_cache = True, load_at_startup = True).values_list('name', 'value'):
            CONFIG_CACHE[name] = value

    @classmethod
    def clear_cache(cls):
        global CONFIG_CACHE

        CONFIG_CACHE = {}

def clear_config_cache(sender, **kwargs):
    instance = kwargs['instance']

    try:
        del CONFIG_CACHE[instance.name]
    except KeyError:
        pass

# Usage
# from django.db.models.signals import pre_save, pre_delete
# pre_save.connect(clear_config_cache, sender = Config)
# pre_delete.connect(clear_config_cache, sender = Config)

@python_2_unicode_compatible
class AbstractSite(models.Model):
    domain = models.CharField(_("Domain"), max_length = 100)
    language = models.CharField(max_length = 2, choices = settings.LANGUAGES, verbose_name = _("Language"))
    is_active = models.BooleanField(_("Is active"), default = False)

    objects = SiteManager()
    active_objects = ActiveManager()

    class Meta:
        verbose_name = _("Site")
        verbose_name_plural = _("Sites")
        ordering = ('domain', 'is_active')
        abstract = True

    def __str__(self):
        return self.domain

def clear_site_cache(sender, **kwargs):
    instance = kwargs['instance']

    try:
        del SITE_CACHE[instance.pk]
    except KeyError:
        pass

# Usage
# from django.db.models.signals import pre_save, pre_delete
# pre_save.connect(clear_site_cache, sender = Site)
# pre_delete.connect(clear_site_cache, sender = Site)

class AbstractLog(models.Model):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    LEVEL_CHOICE = (
        (NOTSET, 'NOTSET'),
        (DEBUG, 'DEBUG'),
        (INFO, 'INFO'),
        (SUCCESS, 'SUCCESS'),
        (WARNING, 'WARNING'),
        (ERROR, 'ERROR'),
        (CRITICAL, 'CRITICAL'),
    )

    name = models.CharField(_("Source"), max_length = 255, db_index = True)
    level = models.IntegerField(_("Level"), default = INFO, choices = LEVEL_CHOICE)
    message = models.CharField(_("Description"), max_length = 255)
    user = models.CharField(_("User"), max_length = 255, null = True, blank = True, db_index = True)
    date = models.DateTimeField(_("Date"), auto_now_add = True, db_index = True)
    args = models.TextField(_("Extra details"), null = True, blank = True)

    class Meta:
        verbose_name = _("System log")
        verbose_name_plural = _("System logs")
        ordering = ('-id',)
        abstract = True

    def __unicode__(self):
        return u"%s: %s" % (self.get_level_name(self.level), self.name)

    @classmethod
    def is_valid_level(cls, level):
        level_dict = dict(cls.LEVEL_CHOICE)
        return level in level_dict.keys()

    @classmethod
    def get_level_name(cls, level):
        level_dict = dict(cls.LEVEL_CHOICE)
        return level_dict[level]

    @classmethod
    def get_max_level(cls, level_list, default = NOTSET):
        level = default
        for _level in level_list:
            if _level > level:
                level = _level
        return level

    @classmethod
    def render_level(cls, level):
        if level == cls.DEBUG:
            css_class = 'text-muted'
        elif level == cls.INFO:
            css_class = 'text-info'
        elif level == cls.SUCCESS:
            css_class = 'text-success'
        elif level == cls.WARNING:
            css_class = 'text-warning'
        elif level == cls.ERROR:
            css_class = 'text-danger'
        elif level == cls.CRITICAL:
            css_class = 'text-danger'
        else:
            css_class = ''
        label = cls.get_level_name(level)
        return """<span class="%s">%s</span>""" % (css_class, label)

class AbstractUrlRedirect(models.Model):
#    sites = models.ManyToManyField(Site, blank = True, null = True, verbose_name = u"Strony")
    old_url = models.CharField(_("Old URL"), max_length = 255, db_index = True, help_text = _("URL format: ^/old-url/$"))
    redirect_url = models.CharField(_("New URL"), max_length = 255, help_text = _("URL format: /new-url/"))
    rewrite_tail = models.BooleanField(_("Rewrite tail?"), default = False, help_text = _("Should /old-url/abc/ be changet do /new-url/abc/ or just /new-url/?"))
    is_permanent_redirect = models.BooleanField(_("Permanent redirect?"), default = True, help_text = _("Is redirect permanent (301) or temporary (302)?"))

    class Meta:
        verbose_name = _("URL redirect")
        verbose_name_plural = _("URL redirects")
        ordering = ('old_url',)
        abstract = True

    def __unicode__(self):
        return u"%s › %s" % (self.old_url, self.redirect_url)

    @classmethod
    def _get_query(cls):
        db_table = cls.objects.model._meta.db_table
        query = """
            SELECT *
            FROM %s
            WHERE $s REGEXP old_url
            ORDER BY LENGTH(old_url) - LENGTH(REPLACE(old_url, '/', '')) DESC
            LIMIT 1
        """ % db_table
        query = query.replace('$s', '%s')
        return query

    @classmethod
    def get_redirect_tuple(cls, old_url):
        query = cls._get_query()

        try:
            redirect = list(cls.objects.raw(query, [old_url]))[0]

            if settings.DEBUG:
                print ""
                print "%s > %s" % (redirect.old_url, redirect.redirect_url)
                print "  rewrite_tail: %s, is_permanent_redirect %s" % (redirect.rewrite_tail, redirect.is_permanent_redirect)
                print ""

            if redirect.rewrite_tail:
                redirect_url = old_url.replace(redirect.old_url.replace('^', '').replace('$', ''), redirect.redirect_url)
            else:
                redirect_url = redirect.redirect_url
            return (redirect_url, redirect.is_permanent_redirect)
        except IndexError:
            return (None, None)
