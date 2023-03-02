from datetime import datetime
from django.urls import reverse
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def current_url(context):
    request = context['request']
    url = request.build_absolute_uri(reverse(request.resolver_match.view_name))
    if request.GET:
        url += '?' + request.GET.urlencode()
    return url


@register.simple_tag()
def current_time(format_string='%b %d %Y'):
    return datetime.utcnow().strftime(format_string)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()

