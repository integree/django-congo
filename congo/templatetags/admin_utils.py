from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.contenttypes.models import ContentType
from congo.templatetags import Library

register = Library()

@register.filter
def admin_change_url(value):
#    {% url 'admin:index' %}
#    {% url 'admin:polls_choice_add' %}
#    {% url 'admin:polls_choice_change' choice.id %}
#    {% url 'admin:polls_choice_changelist' %}

    url = ""
    try:
        url = reverse('admin:%s_%s_change' % (value._meta.app_label, value._meta.model_name), args = (value.id,))
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
