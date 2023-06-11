from django.contrib import admin

from .models import (Cronograma, DotacaoOrcamentaria, EquipamentoServico,
                     Orcamento, PacoteDespesa, PacoteReceita, Projeto,
                     Tasks_Cronograma)

admin.site.register(Projeto)
admin.site.register(DotacaoOrcamentaria)
admin.site.register(EquipamentoServico)
admin.site.register(Tasks_Cronograma)
admin.site.register(Cronograma)
admin.site.register(Orcamento)
admin.site.register(PacoteDespesa)
admin.site.register(PacoteReceita)
