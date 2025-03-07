from django import forms
from .models import Medicacion

class MedicacionForm(forms.ModelForm):
    class Meta:
        model = Medicacion
        fields = ['nombre_medicamento', 'dosis', 'frecuencia']
        widgets = {
            'nombre_medicamento': forms.TextInput(attrs={'class': 'form-control'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control'}),
        }
