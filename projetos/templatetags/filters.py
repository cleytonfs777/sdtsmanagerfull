from django import template
from django.db.models import Case, FloatField, Sum, When

from projetos.models import (EquipamentoServico, PacoteAquisicao,
                             PacoteAquisicaoEquipamentoServico, Projeto, PacoteEmpenho)

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

@register.filter(name='value_pacote_emp')
def value_pacote_emp(value):
    pacote = PacoteEmpenho.objects.get(id=value)
    valor_total = 0

    # Iterar sobre DotacaoOrcamentaria
    for dotacao_orc in pacote.dotacoes_orcamentarias.all():
        valor_total += dotacao_orc.valor

    # Formata o valor total para o formato de moeda em reais
    valor_total = f'R$ {valor_total:,.2f}'.replace(
        ',', 'v').replace('.', ',').replace('v', '.') if valor_total else 'R$ 0,00' # noqa 
    

    return valor_total

@register.filter(name='value_pacote')
def value_pacote(value):
    pacote = PacoteAquisicao.objects.get(id=value)
    valor_total = 0

    # Iterar sobre PacoteAquisicaoEquipamentoServico
    for aquisicao_equipamento in pacote.aquisicao_equipamento.all():
        if aquisicao_equipamento.usa_preco_portal:
            valor_total += (aquisicao_equipamento.equipamento.valor_portal *
                            aquisicao_equipamento.quantidade)
        else:
            valor_total += (aquisicao_equipamento.valor_medio *
                            aquisicao_equipamento.quantidade)
    # Formata o valor total para o formato de moeda em reais
    valor_total = f'R$ {valor_total:,.2f}'.replace(
        ',', 'v').replace('.', ',').replace('v', '.') if valor_total else 'R$ 0,00'

    return valor_total


@register.filter(name='value_projeto')
def value_projeto(value):
    # A partir do id de um projeto ele analisa todos os pacotes de aquisição e soma os valores de cada pacote aos moldes do que ocorre no filter value_pacote
    projeto = Projeto.objects.get(id=value)
    valor_total = 0

    # Iterar sobre PacoteAquisicaoEquipamentoServico
    for pacote in projeto.pacote_aquisicao.all():
        for aquisicao_equipamento in pacote.aquisicao_equipamento.all():
            if aquisicao_equipamento.usa_preco_portal:
                valor_total += (aquisicao_equipamento.equipamento.valor_portal *
                                aquisicao_equipamento.quantidade)
            else:
                valor_total += (aquisicao_equipamento.valor_medio *
                                aquisicao_equipamento.quantidade)
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


@register.filter(name="formatdate")
def formatdate(value):
    if value:
        return value.strftime("%d/%m/%Y")
    else:
        return None


@register.filter(name="inputformatdate")
def inputformatdate(value):
    if value:
        return value.strftime("%Y-%m-%d")
    else:
        return None


@register.filter(name="sei_interable")
def sei_interable(value):
    # Em value recebe uma string que deve ser separada por ";" e posteriormente retornada uma lista com o conteudo
    if value == None:
        return [""]
    elif ";" in value:
        return value.split(";")
    else:
        return [value]


@register.filter(name="render_table")
def render_table(value, target):
    if target == 'equipamento':
        pacote = PacoteAquisicao.objects.get(id=value)
        despesas_target = pacote.aquisicao_equipamento.all()
    elif target == 'cronograma':
        pacote = PacoteAquisicao.objects.get(id=value)
        despesas_target = pacote.tasks.all()
    elif target == 'obspen':
        pacote = PacoteAquisicao.objects.get(id=value)
        despesas_target = pacote.observacoes_pendencias.all()

    return despesas_target


@register.filter(name="render_table_tasks")
def render_table_tasks(value):
    pacote = PacoteAquisicao.objects.get(id=value)
    tasks = pacote.tasks.all()

    return tasks


@register.filter(name="kindvalue")
def kindvalue(value):
    # recebe o id de um equipamento e verifica a variavel usa_preco_portal. Se for verdadeiro deverá retornar o preço da chave preco_portal, caso contrario retorna o valor medio
    equipamento = PacoteAquisicaoEquipamentoServico.objects.get(id=value)
    if equipamento.usa_preco_portal:
        return f'R$ {equipamento.equipamento.valor_portal:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.') if equipamento.equipamento.valor_portal else 'R$ 0,00'
    else:
        return f'R$ {equipamento.valor_medio:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.') if equipamento.valor_medio else 'R$ 0,00'


@register.filter(name="valortotalequip")
def valortotalequip(value):
    # recebe o id de um equipamento e verifica a variavel usa_preco_portal. Se for verdadeiro deverá retornar o preço da chave preco_portal multiplicado pelo valor na chave quantidade, caso contrario retorna o valor medio multiplicado pelo valor na chave quantidade
    equipamento = PacoteAquisicaoEquipamentoServico.objects.get(id=value)
    if equipamento.usa_preco_portal:
        return f'R$ {(equipamento.equipamento.valor_portal  * equipamento.quantidade):,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.') if equipamento.equipamento.valor_portal else 'R$ 0,00'
    else:
        return f'R$ {(equipamento.valor_medio  * equipamento.quantidade):,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.') if equipamento.valor_medio else 'R$ 0,00'


@register.filter(name="config_id")
def config_id(value):
    # recebe um id da classe EquipamentoServico e retorna o valor das chaves tipo e valor_portal
    equipamento = EquipamentoServico.objects.get(id=value)
    return f"{equipamento.tipo}-{equipamento.valor_portal}"


@register.filter(name="toLocaleStringCurrencyBRL")
def toLocaleStringCurrencyBRL(value):
    return f'R$ {value:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.') if value else 'R$ 0,00'


@register.filter(name="initialDate")
def initialDate(data_inicial, data_real_inicial):
    # Se houver a data_real_inicial, retorna ela, caso contrario retorna a data_inicial
    if data_real_inicial:
        return data_real_inicial
    else:
        return data_inicial


@register.filter(name="finalDate")
def finalDate(data_final, data_real_final):
    # Se houver a data_real_final, retorna ela, caso contrario retorna a data_final
    if data_real_final:
        return data_real_final
    else:
        return data_final


@register.filter(name="ajusta_fase")
def ajusta_fase(value):
    if value == 'rp-etp':
        return 'Elaboração do ETP'
    if value == 'rp-orcamentos':
        return 'Obtenção de Orçamentos'
    if value == 'rp-precos':
        return 'Mapa de Preços'
    if value == 'rp-autorizacao-dlf':
        return 'Pedido de autorização DLF'
    if value == 'rp-gestao':
        return 'Solicitação de Gestão de RP'
    if value == 'rp-minuta':
        return 'Elaboração Minuta do Termo de Referência'
    if value == 'rp-correcao-minuta':
        return 'Correção Minuta do Termo de Referência (ASSJUR)'
    if value == 'rp-correcao-etp':
        return 'Correção ETP (ASSJUR)'
    if value == 'rp-formulario-adesao':
        return 'Formulário de Adesão'
    if value == 'rp-encaminhado-gol':
        return 'Encaminhado a Gol'
    if value == 'rp-impugnacao':
        return 'Respondendo impugnação'
    if value == 'rp-resposta-documentacao':
        return 'Resposta a documentação'
    if value == 'pg-autorizacao-dlf':
        return 'Pedido de autorização DLF'
    if value == 'pg-etp':
        return 'Elaboração do ETP'
    if value == 'pg-orcamentos':
        return 'Obtenção de Orçamentos'
    if value == 'pg-precos':
        return 'Mapa de Preços'
    if value == 'pg-minuta':
        return 'Elaboração Minuta do Termo de Referência'
    if value == 'pg-extrato':
        return 'Extrato de Crédito'
    if value == 'pg-correcao-minuta':
        return 'Correção Minuta do Termo de Referência (ASSJUR)'
    if value == 'pg-correcao-etp':
        return 'Correção ETP (ASSJUR)'
    if value == 'Terceiros':
        return 'Terceiros'

@register.filter(name="formatnat")
def formatnat(value):

    if value == 'material':
        return 'Material'
    elif value == 'servico':
        return 'Serviço'
    elif value == 'materialservico':
        return 'Material/Serviço'