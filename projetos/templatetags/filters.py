from django import template

from projetos.models import Projeto

register = template.Library()


@register.filter(name='tipo_projeto')
def tipo_projeto(value):
    if value == '1':
        return 'Despesa'
    elif value == '2':
        return 'Receita'
    else:
        return 'Outros'
