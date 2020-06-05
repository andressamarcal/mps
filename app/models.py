# -*- encoding: utf-8 -*-

from datetime import datetime

from django.db import models


class Arquivo(models.Model):
    tipo = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='csv/')


class Consulta(models.Model):
    numero_guia_consulta = models.PositiveIntegerField(primary_key=True)
    cod_medico = models.PositiveIntegerField()
    nome_medico = models.CharField(max_length=100)
    data_consulta = models.DateField(auto_now=False, auto_now_add=False)
    valor_consulta = models.FloatField()

    class Meta:
        ordering = ('data_consulta',)

    def __str__(self):
        return "{}".format(int(self.numero_guia_consulta))

    def get_data_consulta(self):
        return self.data_consulta.strftime('%d/%m/%Y')

    @property
    def gasto_consulta(self):
        return sum([exame['valor_exame'] for exame in self.exame_set.values()])

    @property
    def quantidade_consultas(self):
        return sum([consulta['valor_consulta'] for consulta in self.consulta_set.values()])
    
    @property
    def quantidade_exames(self):
        return self.exame_set.count()

    @property
    def to_dict_json(self):
        return {
            'quantidade_exames': self.quantidade_exames,
            'quantidade_consultas': self.quantidade_consultas,
            'gasto_consulta': self.gasto_consulta,
        }


class Exame(models.Model):
    numero_guia_consulta = models.ForeignKey(
        Consulta, on_delete=models.CASCADE)
    descricao = models.TextField(verbose_name='Descrição do Exame')
    valor_exame = models.FloatField()

    def __str__(self):
        return "{}".format(int(self.numero_guia_consulta))
