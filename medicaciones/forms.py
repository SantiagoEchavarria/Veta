from django import forms
from .models import Medicacion

class MedicacionForm(forms.ModelForm):
    hora_inicio = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = Medicacion
        fields = ['nombre_medicamento', 'dosis', 'frecuencia', 'hora_inicio']
        widgets = {
            'nombre_medicamento': forms.TextInput(attrs={'class': 'form-control'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control'}),
            }
        
        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
            if user:
                self.fields['zona_horaria'] = forms.CharField(
                    initial=user.paciente.zona_horaria
                )