from django import template
from ..models import Artist, Organizer
register = template.Library()

@register.filter(name='add_class')
def do_add_class(field, css):
   return field.as_widget(attrs={"class":css})

@register.filter
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

@register.filter
def as_artist(user):
    return Artist(user)

@register.filter
def as_org(user):
    return Organizer(user)

@register.filter
def owns(user, object):
    return user.owns(object)

@register.filter
def owns_drawing(user, drawing):
    return user.is_artist and Artist(user).owns(drawing)

@register.filter
def owns_xzibit(user, exhibition):
    return user.is_organizer and Organizer(user).owns(exhibition)
