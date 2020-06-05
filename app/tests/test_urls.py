from django.urls import reverse, resolve
# from django.test import TestCase
# from .models import Consulta, Exame
# from django.shortcuts import get_object_or_404


# class ConsultaModelTestCase(TestCase):
#     def setUp(self):
#         Consulta.objects.create(numero_guia_consulta=101010, cod_medico=101010, 
#                                 nome_medico='João Teste', data_consulta=2010-10-10,
#                                 valor_consulta=10,0)
    
#     def test_get_consulta(self):
#         obj = Consulta.objects.get_object_or_404(numero_guia_consulta=101010)
        


class TestUrls:

    def test_home_url(self):
        path = reverse('home')
        assert resolve(path).view_name == 'DashboardView'



