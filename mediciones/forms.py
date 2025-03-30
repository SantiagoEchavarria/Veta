from django import forms
from .models import MedicionGlucosa

class MedicionGlucosaForm(forms.ModelForm):
    class Meta:
        model = MedicionGlucosa
        fields = ['nivel_glucosa', 'tipo_medicion', 'notas']
