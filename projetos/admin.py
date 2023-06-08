from django.contrib import admin

from .models import (Cronograma, DotacaoOrcamentaria, Equipamentos, Orcamento,
                     PacoteDespesa, PacoteReceita, Projeto, Servicos,
                     Tasks_Cronograma)

admin.site.register(Projeto)
admin.site.register(DotacaoOrcamentaria)
admin.site.register(Equipamentos)
admin.site.register(Servicos)
admin.site.register(Tasks_Cronograma)
admin.site.register(Cronograma)
admin.site.register(Orcamento)
admin.site.register(PacoteDespesa)
admin.site.register(PacoteReceita)
