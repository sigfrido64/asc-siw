from django import template

# from rolepermissions.checkers import has_permission
from ..models import has_permission


register = template.Library()


@register.filter(name='can')
def can_template_tag(user, permission):
    return has_permission(user, permission)
