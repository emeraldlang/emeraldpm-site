from django import template
from django.utils.safestring import mark_safe

import bleach
import markdown


register = template.Library()


_allowed_attributes = bleach.sanitizer.ALLOWED_ATTRIBUTES.copy()
_allowed_attributes['img'] = ['src', 'alt', 'width', 'height']

_allowed_tags = bleach.sanitizer.ALLOWED_TAGS.copy()
_allowed_tags += ['img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'br']


@register.filter
def markdown_to_html(text):
    return mark_safe(
        bleach.clean(
            markdown.markdown(
                text,
                extensions=[
                    'md_in_html',
                    'markdown.extensions.fenced_code'
                ]
            ),
            attributes=_allowed_attributes,
            tags=_allowed_tags,
        )
    )
