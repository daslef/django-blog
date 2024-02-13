from django import template

register = template.Library()


@register.filter(name="with_class")
def with_class(element, classnames):
    element.field.widget.attrs.update({"class": classnames})
    return element
