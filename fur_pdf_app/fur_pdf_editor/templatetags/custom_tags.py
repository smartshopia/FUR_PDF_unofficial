from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_media_prefix():
    return settings.MEDIA_URL
