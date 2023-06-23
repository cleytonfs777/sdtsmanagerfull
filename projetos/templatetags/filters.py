from django import template
from django.db.models import Case, FloatField, Sum, When

from projetos.models import (Cronograma, PacoteAquisicao,
                             PacoteAquisicaoEquipamentoServico, Projeto)

register = template.Library()


@register.filter(name='tipo_projeto')
def tipo_projeto(value):
    if value == '1':
        return 'Aquisicao'
    elif value == '2':
        return 'Receita'
    else:
        return 'Outros'


@register.filter(name='value_to_real')
def value_to_real(value):
    return f'R$ {value:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.') if value else 'R$ 0,00'


@register.filter(name='value_pacote')
def value_pacote(value):
    pacote = PacoteAquisicao.objects.get(id=value)
    valor_total = 0

    # Iterar sobre PacoteAquisicaoEquipamentoServico
    for despesa_equipamento in pacote.despesa_equipamento.all():
        if despesa_equipamento.usa_preco_portal:
            valor_total += (despesa_equipamento.equipamento.preco_portal *
                            despesa_equipamento.quantidade)
        else:
            valor_total += (despesa_equipamento.valor_medio *
                            despesa_equipamento.quantidade)
    # Formata o valor total para o formato de moeda em reais
    valor_total = f'R$ {valor_total:,.2f}'.replace(
        ',', 'v').replace('.', ',').replace('v', '.') if valor_total else 'R$ 0,00'

    return valor_total


@register.filter(name='split')
def split(value):
    if ";" in value:
        return value.split(";")
    else:
        return [value]


@register.filter(name='totequip')
def totequip(qtd, value):
    return qtd * value


@register.filter(name="alltasks")
def alltasks(id_cron):
    cronograma = Cronograma.objects.get(id=id_cron)
    tasks = cronograma.tasks.all()

    return tasks
