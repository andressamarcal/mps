# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import Consulta, Exame


class ExameAdmin(admin.ModelAdmin):
    list_display = ('numero_guia_consulta', 'descricao', 'valor_exame')
    search_fields = ('numero_guia_consulta', 'descricao')
    ordering = ('numero_guia_consulta',)

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('numero_guia_consulta','nome_medico', 'cod_medico',
                    'data_consulta', 'valor_consulta')
    list_filter = ('data_consulta',)
    search_fields = ('data_consulta', 'nome_medico', 'cod_medico', 'numero_guia_consulta')
    ordering = ('numero_guia_consulta', 'nome_medico')


admin.site.register(Exame, ExameAdmin)
admin.site.register(Consulta, ConsultaAdmin)
