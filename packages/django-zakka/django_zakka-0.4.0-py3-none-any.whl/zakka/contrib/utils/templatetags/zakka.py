from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def qs(context, *args, **kwargs):
    # If an item is passed as args, we
    # convert it to a kwargs so we can
    # simplify our code
    qs = context["request"].GET.copy()
    if args:
        kwargs[args[0]] = args[1]
    for key in kwargs:
        if kwargs[key]:
            qs[key] = kwargs[key]
    return urlencode(qs)
