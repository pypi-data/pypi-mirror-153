from django import template

import html2text

register = template.Library()


@register.filter
def textify(html):
    h = html2text.HTML2Text()
    h.ignore_links = False
    return h.handle(html)
