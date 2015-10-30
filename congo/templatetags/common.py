# -*- coding: utf-8 -*-
from congo.conf import settings
from decimal import Decimal
from django.core.cache import caches
from django.template.base import TemplateSyntaxError, Node
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from random import random
from congo.templatetags import Library

register = Library()

@register.filter(is_safe = True)
def or_blank(value, use_html = True):
    if value:
        return value
    else:
        text = _("(Blank)")
        html = u"""<span class="text-muted">%s</span>""" % text
        blank = html if bool(use_html) else text
        return mark_safe(blank)

@register.filter
def if_empty(value, arg = ""):
    return value or arg

@register.smart_tag
def smart_tag_test(*args, **kwargs):
    result = ""
    if not args and not kwargs:
        result += "<h4>No args and kwargs</h4><p>...no args, no kwargs :(</p>"
    if args:
        result += "<h4>Args</h4>"
        result += "<ul>"
        for a in args:
            result += "<li>%s</li>" % a
        result += "</ul>"
    if kwargs:
        result += "<h4>Kwargs</h4>"
        result += "<ul>"
        for k, v in kwargs.items():
            result += "<li>%s: %s</li>" % (k, v)
        result += "</ul>"
    return result

@register.smart_tag(takes_context = True)
def smart_tag_context_test(context, *args, **kwargs):
    result = "<h4>User: %s</h4>" % context['request'].user
    if not args and not kwargs:
        result += "<h4>No args and kwargs</h4><p>...no args, no kwargs :(</p>"
    if args:
        result += "<h4>Args</h4>"
        result += "<ul>"
        for a in args:
            result += "<li>%s</li>" % a
        result += "</ul>"
    if kwargs:
        result += "<h4>Kwargs</h4>"
        result += "<ul>"
        for k, v in kwargs.items():
            result += "<li>%s: %s</li>" % (k, v)
        result += "</ul>"
    return result

## messages
#
#@fancy_tag(register)
#def message(msg, **kwargs):
#    # dismiss (bool, False)
#    # close (bool, False)
#
#    if not msg:
#        return ""
#    elif isinstance(msg, Message) or isinstance(msg, _Message):
#        obj = msg
#    else:
#        level = kwargs.get('level', None)
#        if level not in Message.DEFAULT_TAGS.values():
#            level = 'info'
#        obj = getattr(Message, level)(msg)
#    return Message.render(obj, **kwargs)
#
#@register.tag
#def blockmessage(parser, token):
#    try:
#        tag_name, level = token.contents.split(None, 1)
#    except ValueError:
#        level = "info"
#    node_list = parser.parse(('endblockmessage',))
#    parser.delete_first_token()
#    return BlockMessageNode(node_list, level[1:-1])
#
#class BlockMessageNode(Node):
#    def __init__(self, node_list, level):
#        self.node_list = node_list
#        self.level = level
#
#    def render(self, context):
#        level = self.level
#        if level not in Message.DEFAULT_TAGS.values():
#            level = 'info'
#        obj = getattr(Message, level)(self.node_list.render(context))
#        return Message.render(obj)

## ecape
#
#@register.tag('escape')
#def do_escape(parser, token):
#    """
#    {% escape %}
#        <div>Some HTML here...</div>
#    {% endescape %}
#    """
#    node_list = parser.parse(('endescape',))
#    parser.delete_first_token()
#    return EscapeNode(node_list)
#
#class EscapeNode(Node):
#    def __init__(self, node_list):
#        self.node_list = node_list
#
#    def render(self, context):
#        return escape(self.node_list.render(context))

## var & blockvar
#
#@fancy_tag(register)
#def var(obj):
#    return obj
#
#@register.tag
#def blockvar(parser, token):
#    # https://djangosnippets.org/snippets/545/
#    try:
#        tag_name, var_name = token.contents.split(None, 1)
#    except ValueError:
#        raise TemplateSyntaxError("'var' node requires a variable name.")
#    node_list = parser.parse(('endblockvar',))
#    parser.delete_first_token()
#    return VarNode(node_list, var_name)
#
#class VarNode(Node):
#    def __init__(self, node_list, var_name):
#        self.node_list = node_list
#        self.var_name = var_name
#
#    def render(self, context):
#        output = self.node_list.render(context)
#        context[self.var_name] = output
#        return ""

# cache

@register.tag('cache')
def do_cache(parser, token):
    """
    {% cache "cache_key" [expire_time] %}
        .. some expensive processing ..
    {% endcache %}
    """

    node_list = parser.parse(('endcache',))
    parser.delete_first_token()
    tokens = token.split_contents()

    if len(tokens) == 2:
        cache_key = tokens[1]
        expire_time = 0
    elif len(tokens) == 3:
        cache_key, expire_time = tokens[1:]
    else:
        raise TemplateSyntaxError("'cache' tag requires 1 or 2 arguments.")

    return CacheNode(node_list, cache_key[1:-1], expire_time)

class CacheNode(Node):
    def __init__(self, node_list, cache_key, expire_time):
        self.node_list = node_list
        self.cache_key = cache_key
        self.expire_time = expire_time

    def render(self, context):
        try:
            expire_time = int(self.expire_time)
        except (ValueError, TypeError):
            raise TemplateSyntaxError('"cache" tag got a non-integer timeout value: %r' % self.expire_time)

        cache_backend = settings.CONGO_TEMPLATE_CACHE_BACKEND
        cache = caches[cache_backend]
        version = 'template'
        value = cache.get(self.cache_key, version = version)
        if value is None:
            value = self.node_list.render(context)
            if not expire_time:
                # jeśli nie podano czasu, ustawiamy cache na domyślny -10% / +20%
                expire_time = settings.CACHES[cache_backend].get('TIMEOUT', 0)
                expire_time = int(expire_time * (.9 + random() * .3))
            if expire_time:
                cache.set(self.cache_key, value, expire_time, version = version)
            else:
                cache.set(self.cache_key, value, version = version)
        return value
