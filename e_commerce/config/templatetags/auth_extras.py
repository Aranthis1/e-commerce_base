from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    # Verificamos si el usuario pertenece al grupo que le pasemos
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()