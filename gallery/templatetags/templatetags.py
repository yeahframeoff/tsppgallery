from django import template
register = template.Library()

@register.filter(name='add_class')
def do_add_class(field, css):
   return field.as_widget(attrs={"class":css})
