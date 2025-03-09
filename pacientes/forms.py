from django import forms
from .models import Paciente


class PacienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['tipo_diabetes'] 