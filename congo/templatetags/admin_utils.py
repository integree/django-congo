from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.filter
def admin_change_url(value):
    url = ""
    try:
        url = reverse('admin:%s_%s_change' % (value._meta.app_label, value._meta.module_name), args = (value.id,))
    except (NoReverseMatch, AttributeError):
        pass
    return url

@register.filter
def content_type_id(value):
    try:
        content_type = ContentType.objects.get_for_model(value)
        return content_type.id
    except AttributeError:
        return None
