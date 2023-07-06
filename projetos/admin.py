from django.contrib import admin

from .models import (DotacaoOrcamentaria, EquipamentoServico, Orcamento,
                     PacoteAquisicao, PacoteAquisicaoEquipamentoServico,
                     PacoteEmpenho, Projeto, Tasks_Cronograma)

admin.site.register(Projeto)
admin.site.register(DotacaoOrcamentaria)
admin.site.register(EquipamentoServico)
admin.site.register(Tasks_Cronograma)
admin.site.register(Orcamento)
admin.site.register(PacoteAquisicao)
admin.site.register(PacoteEmpenho)
admin.site.register(PacoteAquisicaoEquipamentoServico)
