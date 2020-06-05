from django import forms
from .models import Consulta, Exame


class FilterForm(forms.Form):
    
    class Meta:
        model = Consulta
        fields = ('nome_medico')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome_medico'].queryset = Consulta.objects.values('nome_medico').distinct()
 