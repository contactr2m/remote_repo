from django.template import Library
from artist.models import show_artisttype
register = Library()


@register.simple_tag
def decode_artisttype(artisttype):
    """
    Decode a single artist artisttype
    """
    return show_artisttype(artisttype)


@register.simple_tag
def decode_artisttypes(artisttypes):
    """
    Decode all types of artist
    """
    decoded = [show_artisttype(t) for t in artisttypes]
    decoded.sort()
    return ', '.join(decoded)

