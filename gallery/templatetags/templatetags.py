from django import template
register = template.Library()

@register.filter(name='add_class')
def do_add_class(field, css):
   return field.as_widget(attrs={"class":css})

@register.filter
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)
