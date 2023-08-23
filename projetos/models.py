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
    ('recolhido', 'Recolhido'),
    ('remanejado', 'Remanejado'),
    ('cancelado', 'Cancelado'),
)


class Projeto(models.Model):

    titulo = models.CharField(max_length=100)
    responsavel = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    etiqueta = models.CharField(max_length=20, choices=choices_etiqueta)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class HistoricoDocacaoOrcamentaria(models.Model):
    choice_acao = (
        ('env', 'envio'),
        ('aum', 'aumento'),
        ('red', 'redução'),
        ('reb', 'rebalanceamento')
    )
    acao = models.CharField(max_length=20, choices=choice_acao)
    detalhamento = models.TextField(blank=True, null=True)
    data_acao = models.DateField(blank=True, null=True)
    pacote_empenho = models.ForeignKey(
        'DotacaoOrcamentaria', on_delete=models.CASCADE, related_name='historico_dotacoes_orcamentarias', null=True)

    def __str__(self):
        return self.elemento_item


class DotacaoOrcamentaria(models.Model):
    choices_origem = (
        ('CSM', '1400011 - CSM'),
        ('Aj-Geral', '1400005 - Aj-Geral'),
        ('ABM', '1400017 - ABM'),
        ('DLF', 'USDO 1400018 - DLF'),
        ('1ºBBM', '1400006 - 1ºBBM'),
        ('3ºBBM', '1400008 - 3ºBBM'),
        ('USDO GOL', '1400018 - USDO GOL'),
        ('4ºCOB', '1400034 - 4ºCOB'),
        ('BOA', '1400019 - BOA'),
        ('2ºCOB', '1400021 - 2ºCOB'),
        ('8ºBBM', '1400014 - 8ºBBM'),
        ('5ºBBM', '1400010 - 5ºBBM'),
        ('12ºBBM', '1400027 - 12ºBBM'),
        ('3ºCOB', '1400023 - 3ºCOB'),
        ('5ºCOB', '1400029 - 5ºCOB'),
        ('6ºCOB', '1400030 - 6ºCOB'),
    )
    acao = models.CharField(max_length=100, blank=True, null=True)
    fonte = models.CharField(max_length=100, blank=True, null=True)
    elemento_item = models.CharField(max_length=100, blank=True, null=True)
    conta = models.CharField(max_length=100, blank=True, null=True)
    natureza_desp = models.CharField(
        max_length=20, choices=choice_nat_desp, blank=True, null=True)
    unid_origem = models.CharField(
        max_length=50, choices=choices_origem, blank=True, null=True)
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    divisoes = models.TextField(blank=True, null=True)
    doc_ref = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=choice_status_receita, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    pacote_empenho = models.ForeignKey(
        'PacoteEmpenho', on_delete=models.CASCADE, related_name='dotacoes_orcamentarias', null=True)

    def __str__(self):
        return self.elemento_item


class EquipamentoServico(models.Model):

    choices_sit = (
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('suspenso', 'Suspenso')
    )
    choices_classe = (
        ('consumo', 'Consumo'),
        ('permanente', 'Permanente')
    )

    natureza = models.CharField(max_length=20, choices=choices_nat)
    titulo = models.CharField(max_length=100)
    especificacao = models.TextField(blank=True, null=True)
    registro_preco = models.CharField(max_length=10, blank=True, null=True)
    codigo_item = models.CharField(max_length=10, blank=True, null=True)
    elemento_item = models.CharField(max_length=8, blank=True, null=True)
    classe = models.CharField(max_length=10, choices=choices_classe)
    valor_portal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    situacao = models.CharField(
        max_length=20, choices=choices_sit, blank=True, null=True)

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
    pacote = models.ForeignKey(
        'PacoteAquisicao', on_delete=models.CASCADE, related_name='tasks', null=True)

    def __str__(self):
        return self.titulo

    def diferenca_de_dias(self):
        data_inicio_c = self.data_inicio_real if self.data_inicio_real else self.data_inicio_planejada
        data_fim_c = self.data_fim_real if self.data_fim_real else self.data_fim_planejada
        if data_inicio_c == '' or data_fim_c == '':
            return 0
        diff = data_fim_c - data_inicio_c

        return diff.days


class Orcamento(models.Model):
    empresa = models.CharField(max_length=100)
    data = models.DateField(blank=True, null=True)
    arquivos = models.CharField(max_length=100)

    def __str__(self):
        return self.empresa


class ObservacaoPendencia(models.Model):
    choices_categorias = (
        ('pendencia', 'Pendência'),
        ('observacao', 'Observação'),
    )
    choices_class = (
        ('aconcluir', 'A concluir'),
        ('concluido', 'Concluído'),
    )
    decricao = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=choices_categorias)
    data_obs_pend = models.DateField(blank=True, null=True)
    class_obs_pend = models.CharField(max_length=20, choices=choices_class)
    pacote_despesa = models.ForeignKey(
        'PacoteAquisicao', on_delete=models.CASCADE, related_name='observacoes_pendencias', null=True)


class PacoteAquisicao(models.Model):

    choices_fase = (
        ('PJ', 'Planejamento'),
        ('RP', 'RP em andamento'),
        ('PG', 'PG em andamento'),
        ('EMP', 'Empenhado'),
        ('AGE', 'Aguardando entrega'),
        ('ENT', 'Entregue'),
        ('INS', 'Instalado')
    )

    choices_esp_fase = (
        ('rp-etp', 'Elaboração do ETP'),
        ('rp-orcamentos', 'Obtenção de Orçamentos'),
        ('rp-precos', 'Mapa de Preços'),
        ('rp-autorizacao-dlf', 'Pedido de autorização DLF'),
        ('rp-gestao', 'Solicitação de Gestão de RP'),
        ('rp-minuta', 'Elaboração Minuta do Termo de Referência'),
        ('rp-correcao-minuta', 'Correção Minuta do Termo de Referência (ASSJUR)'),
        ('rp-correcao-etp', 'Correção ETP (ASSJUR)'),
        ('rp-formulario-adesao', 'Formulário de Adesão'),
        ('rp-encaminhado-gol', 'Encaminhado a Gol'),
        ('rp-impugnacao', 'Respondendo impugnação'),
        ('rp-resposta-documentacao', 'Resposta a documentação'),
        ('pg-autorizacao-dlf', 'Pedido de autorização DLF'),
        ('pg-etp', 'Elaboração do ETP'),
        ('pg-orcamentos', 'Obtenção de Orçamentos'),
        ('pg-precos', 'Mapa de Preços'),
        ('pg-minuta', 'Elaboração Minuta do Termo de Referência'),
        ('pg-extrato', 'Extrato de Crédito'),
        ('pg-correcao-minuta', 'Correção Minuta do Termo de Referência (ASSJUR)'),
        ('pg-correcao-etp', 'Correção ETP (ASSJUR)'),
        ('Terceiros', 'Terceiros'),
    )

    titulo = models.CharField(max_length=100)
    status = models.CharField(
        max_length=100, choices=choices_fase, blank=True, null=True)
    fase = models.CharField(
        max_length=100, choices=choices_esp_fase, blank=True, null=True)
    etiqueta = models.CharField(
        max_length=20, choices=choices_etiqueta)  # Vai vir via url
    natureza = models.CharField(max_length=20, choices=choices_nat)
    contrato = models.CharField(max_length=100, blank=True, null=True)
    contratoinit = models.DateField(blank=True, null=True)
    contratoend = models.DateField(blank=True, null=True)
    doc_ref = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    projeto = models.ForeignKey(
        Projeto, on_delete=models.DO_NOTHING, related_name='pacote_aquisicao')

    def __str__(self):
        return self.titulo


class PacoteAquisicaoEquipamentoServico(models.Model):

    choices_entrega_instalacao = (
        ('demanda', 'Demanda'),
        ('licitacao', 'Licitacao'),
        ('aentregar', 'A entregar'),
        ('entregue', 'Entregue'),
        ('ainstalar', 'A instalar'),
        ('instalado', 'Instalado')
    )
    pacotedespesa = models.ForeignKey(
        PacoteAquisicao, on_delete=models.CASCADE, related_name='despesa_equipamento')
    equipamento = models.ForeignKey(
        EquipamentoServico, on_delete=models.CASCADE, related_name='pacote_equipamento')
    valor_1 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    valor_2 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    valor_3 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    valor_medio = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    usa_preco_portal = models.BooleanField(default=False)
    entrega_instalacao = models.CharField(
        max_length=20, choices=choices_entrega_instalacao)
    data_entrega = models.DateField(blank=True, null=True)
    data_instalacao = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    local = models.CharField(max_length=100)  # Define as per your needs
    destino = models.CharField(max_length=100)  # Define as per your needs
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return self.equipamento.titulo


class PacoteEmpenho(models.Model):
    choices_tipo_pacote = (
        ('despesa', 'Despesa'),
        ('receita', 'Receita')
    )
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    etiqueta = models.CharField(
        max_length=20, choices=choices_etiqueta, blank=True, null=True)
    tipo_pacote = models.CharField(
        max_length=20, choices=choices_tipo_pacote, blank=True, null=True)
    dot_orc = models.ManyToManyField(
        DotacaoOrcamentaria, related_name='pacote_receita_dot_orc')
    documento_ref = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.etiqueta
