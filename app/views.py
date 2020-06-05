# -*- encoding: utf-8 -*-

import csv
import io

from django import template
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.views.generic import CreateView, TemplateView

from .models import Arquivo, Consulta, Exame


@login_required(login_url="/login/")
def pages(request):
    context = {}

    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


class CSVCreateView(CreateView):
    model = Arquivo
    fields = '__all__'
    template_name = "upload.html"
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        instance = self.object

        if instance.tipo == '1':
            Consulta.objects.bulk_create(
                list(self.yield_of_model(instance.arquivo.path, Consulta, instance.tipo)))

        elif instance.tipo == '2':
            Exame.objects.bulk_create(
                list(self.yield_of_model(instance.arquivo.path, Exame, instance.tipo)))

        return response

    def yield_of_model(self, path, model, tipo):
        with open(path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if tipo == '2':
                    row['numero_guia_consulta_id'] = row['numero_guia_consulta']
                    row.pop('numero_guia_consulta')
                yield model(**row)


class ReportView(TemplateView):
    template_name = 'report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        consultas = Consulta.objects.all()
        exames = Exame.objects.all()

        context['consultas'] = consultas
        context['exames'] = exames

        return context

    # def is_valid_queryparam(param):
    #     return param != '' and param is not None

    # def filter(self, request):

    #     date_min = request.GET.get('date_min')
    #     date_max = request.GET.get('date_max')
    #     medico = request.GET.get('medico')

    #     if is_valid_queryparam(date_min):
    #         consultas = consultas.filter(data_consulta__gte=date_min)

    #     if is_valid_queryparam(date_max):
    #         consultas = consultas.filter(data_consulta__lte=date_max)

    #     if is_valid_queryparam(medico):
    #         consultas = consultas.values('nome_medico').distinct()

    #     context = {
    #         'consultas': consultas
    #     }

        # return render(request, 'report.html', context)


class DashboardView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consultas = Consulta.objects.all()
        exames = Exame.objects.all()

        context['total_consultas'] = consultas.count()
        context['total_valor_consultas'] = Consulta.objects.aggregate(
            Sum('valor_consulta'))['valor_consulta__sum']

        context['total_exames'] = exames.count()
        context['total_valor_exames'] = Exame.objects.aggregate(Sum('valor_exame'))[
            'valor_exame__sum']

        dict_mes_ano_consulta, dict_mes_ano_exames = self.return_list_valor_mes(Consulta)

        context['years'] = list(set([consulta.data_consulta.year for consulta in Consulta.objects.all()]))
        context['month_years'] = list(dict_mes_ano_consulta.keys())
        context['data_consulta'] = [sum(values) for values in dict_mes_ano_consulta.values()]
        context['data_exames'] = [sum(values) for values in dict_mes_ano_exames.values()]

        return context

    def return_list_valor_mes(self, model_consulta, cod_medico=None):
        dict_mes_ano_consulta = {}
        dict_mes_ano_exames = {}

        consultas = model_consulta.objects.all().order_by('data_consulta')
        if cod_medico:
            consultas = model_consulta.objects.filter(cod_medico=cod_medico).order_by('data_consulta')

        for consulta in consultas:
            try:
                dict_mes_ano_consulta[f"{consulta.data_consulta.month}/{consulta.data_consulta.year}"].append(consulta.valor_consulta)
            except:
                dict_mes_ano_consulta.update({
                    f"{consulta.data_consulta.month}/{consulta.data_consulta.year}": [consulta.valor_consulta]
                })
            try:
                dict_mes_ano_exames[f"{consulta.data_consulta.month}/{consulta.data_consulta.year}"].append(consulta.gasto_consulta)
            except:
                dict_mes_ano_exames.update({
                    f"{consulta.data_consulta.month}/{consulta.data_consulta.year}": [consulta.gasto_consulta]
                })
        return dict_mes_ano_consulta, dict_mes_ano_exames
        

# def graph(request):
#     consultas = Consulta.objects.all()

#     context = {
#         'consultas': consultas,
#         'consulta_quantidade_exames': consultas.quantidade_exames,
#     }

#     return JsonResponse(request, 'graph.html', context)


class GraphView(TemplateView):
    template_name = 'graph.html'
