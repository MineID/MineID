from django.template import Library

from ..avatar import get_minecraft_avatar


register = Library()


@register.simple_tag
def avatar(minecraft_user, geometry_string):
    return get_minecraft_avatar(minecraft_user, geometry_string)
