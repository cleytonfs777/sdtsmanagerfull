import datetime

from django.db import models
from django.utils import timezone

choices_etiqueta = (
    ('radio', 'Rádio'),
    ('telefonia', 'Telefonia'),
    ('audioevideo', 'Áudio e Vídeo'),
    ('outros', 'Outros')
)

choices_nat = (
    ('material', 'Material'),
    ('servico', 'Serviço'),
    ('materialservico', 'Material/Serviço')
)

choice_nat_desp = (
    ('custeio', 'Custeio'),
    ('capital', 'Capital'),
    ('custeio/capital', 'Custeio/Capital')
)

choice_status_receita = (
    ('adescentralizar', 'A descentralizar'),
    ('descentralizado', 'Descentralizado'),
    ('empenhado', 'Empenhado'),
    ('liquidado', 'Liquidado'),
    ('pago', 'Pago'),
    ('cancelado', 'Cancelado'),
)


class Projeto(models.Model):
    choices_tipo = (
        ('despesa', 'Despesa'),
        ('receita', 'Receita'),
    )
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=choices_tipo)
    responsavel = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    etiqueta = models.CharField(max_length=20, choices=choices_etiqueta)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class DotacaoOrcamentaria(models.Model):
    acao = models.CharField(max_length=100)
    fonte = models.CharField(max_length=100)
    elemento_item = models.CharField(max_length=100)
    conta = models.CharField(max_length=100)
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    documento_ref = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.elemento_item


class EquipamentoServico(models.Model):
    choices_classe = (
        ('consumo', 'Consumo'),
        ('permanente', 'Permanente')
    )
    choices_tipo = (
        ('equipamento', 'Equipamento'),
        ('servico', 'Serviço')
    )

    titulo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=choices_tipo)
    especificacao = models.TextField(blank=True, null=True)
    registro_preco = models.CharField(max_length=10, blank=True, null=True)
    codigo_item = models.CharField(max_length=10, blank=True, null=True)
    elemento_item = models.CharField(max_length=8, blank=True, null=True)
    classe = models.CharField(max_length=10, choices=choices_classe)
    valor_portal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.titulo


class Cronograma(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo


class Tasks_Cronograma(models.Model):
    choices_status = (
        ('pendente', 'Pendente'),
        ('emexecucao', 'Em execução'),
        ('concluido', 'Concluído')
    )
    choices_prioridade = (
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta')
    )
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=choices_status)
    prioridade = models.CharField(max_length=20, choices=choices_prioridade)
    data_inicio_planejada = models.DateField(blank=True, null=True)
    data_fim_planejada = models.DateField(blank=True, null=True)
    data_inicio_real = models.DateField(blank=True, null=True)
    data_fim_real = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    cronograma = models.ForeignKey(
        Cronograma, on_delete=models.CASCADE, related_name='tasks', null=True)

    def __str__(self):
        return self.titulo


class Orcamento(models.Model):
    empresa = models.CharField(max_length=100)
    data = models.DateField(blank=True, null=True)
    arquivos = models.CharField(max_length=100)

    def __str__(self):
        return self.empresa


class PacoteDespesa(models.Model):

    fase = models.CharField(max_length=100)
    esp_fase = models.CharField(max_length=100, blank=True, null=True)
    etiqueta = models.CharField(max_length=20, choices=choices_etiqueta)
    natureza = models.CharField(max_length=20, choices=choices_nat)
    beneficiado = models.CharField(max_length=100, blank=True, null=True)
    localizado_em = models.CharField(max_length=100, blank=True, null=True)
    doc_ref = models.CharField(max_length=100, blank=True, null=True)
    contrato = models.CharField(max_length=100, blank=True, null=True)
    cronograma = models.ForeignKey(
        Cronograma, on_delete=models.DO_NOTHING)
    observacoes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.DO_NOTHING)
    pacotereceita = models.ManyToManyField(
        'PacoteReceita', related_name='pacote_despesa_pacotereceita')

    def __str__(self):
        return self.etiqueta


class PacoteDespesaEquipamentoServico(models.Model):
    choices_sit = (
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('suspenso', 'Suspenso')
    )
    choices_entrega_instalacao = (
        ('demanda', 'Demanda'),
        ('licitacao', 'Licitacao'),
        ('aentregar', 'A entregar'),
        ('entregue', 'Entregue'),
        ('ainstalar', 'A instalar'),
        ('instalado', 'Instalado')
    )
    pacotedespesa = models.ForeignKey(PacoteDespesa, on_delete=models.CASCADE)
    equipamento = models.ForeignKey(
        EquipamentoServico, on_delete=models.CASCADE)
    situacao = models.CharField(
        max_length=20, choices=choices_sit, blank=True, null=True)
    valor_1 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    valor_2 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    valor_3 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    valor_medio = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    entrega_instalacao = models.CharField(
        max_length=20, choices=choices_entrega_instalacao)
    data_entrega = models.DateField(blank=True, null=True)
    data_instalacao = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    local = models.CharField(max_length=100)  # Define as per your needs
    destino = models.CharField(max_length=100)  # Define as per your needs
    quantidade = models.IntegerField(default=1)
    usa_preco_portal = models.BooleanField(default=False)

    def __str__(self):
        return self.equipamento.titulo


class PacoteReceita(models.Model):
    etiqueta = models.CharField(max_length=20, choices=choices_etiqueta)
    natureza_desp = models.CharField(max_length=20, choices=choice_nat_desp)
    dot_orc = models.ManyToManyField(
        DotacaoOrcamentaria, related_name='pacote_receita_dot_orc')
    unid_exec = models.CharField(max_length=100, blank=True, null=True)
    doc_ref = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=choice_status_receita)
    observacoes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.etiqueta
