from django import forms
from .models import MedicionGlucosa

class MedicionGlucosaForm(forms.ModelForm):
    nivel_glucosa = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'max': '600',
            'pattern': '[0-9]+([\\.,][0-9]{1,2})?'
        })
    )

    class Meta:
        model = MedicionGlucosa
        exclude = ['paciente'] 
        widgets = {
            'nivel_glucosa': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'max': '600'
            }),
            'fecha_hora': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'step': '300'
            }, format='%Y-%m-%dT%H:%M'),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nivel_glucosa'].decimal_places = 2
        self.fields['nivel_glucosa'].localize = True