import re
from django import forms
from django.contrib.auth.forms import UserCreationForm,  PasswordChangeForm
from .models import Usuario
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from datetime import date

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'fecha_nacimiento', 'password1', 'password2']
        
class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'fecha_nacimiento']
    
    # Validación para el campo nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        # Permitir letras, espacios y caracteres acentuados
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            raise ValidationError("El nombre solo puede contener letras y espacios.")
        return nombre
    
    # Validación para el campo email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not '@' in email:
            raise ValidationError("Por favor ingrese un correo electrónico válido.")
        return email
    
    # Validación para el campo teléfono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if len(telefono) < 10:
            raise ValidationError("El teléfono debe tener al menos 10 dígitos.")
        return telefono
    
    # Validación para el campo fecha_nacimiento
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento >= date.today():
            raise ValidationError("La fecha de nacimiento no puede ser futura.")
        return fecha_nacimiento

class UsuarioContrasenaForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña actual'})
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'}),
        help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})
    )
    
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']