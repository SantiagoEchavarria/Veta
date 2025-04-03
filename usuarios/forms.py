import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Usuario
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from datetime import date, timedelta

class BaseUsuarioForm:
    """Clase base con validaciones comunes"""
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre').strip()
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,}(?: [a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+){1,}$', nombre):
            raise ValidationError(
                "Debe contener al menos nombre y apellido, solo letras y espacios."
            )
        return nombre
    
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if not re.match(r'^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError(
                "Formato de email inválido. Ejemplo válido: usuario@dominio.com"
            )
        
        # Manejo diferente para creación vs actualización
        if self.instance.pk:  # Si es actualización
            if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Este email ya está registrado.")
        else:  # Si es creación
            if Usuario.objects.filter(email=email).exists():
                raise ValidationError("Este email ya está registrado.")
        
        return email
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(r'^\+?[0-9]{10,15}$', telefono):
            raise ValidationError(
                "El teléfono debe contener entre 10 y 15 dígitos numéricos."
            )
        return telefono
    
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        hoy = date.today()
        
        if fecha_nacimiento > hoy:
            raise ValidationError("La fecha no puede ser futura.")
        
        edad_minima = hoy - timedelta(days=13*365)
        if fecha_nacimiento > edad_minima:
            raise ValidationError("Debes tener al menos 13 años.")
        
        return fecha_nacimiento

class UsuarioCreationForm(BaseUsuarioForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'fecha_nacimiento', 'password1', 'password2']
        help_texts = {
            'telefono': 'Formato: 1234567890 (10 dígitos mínimo)',
            'fecha_nacimiento': 'Formato: DD/MM/AAAA',
        }
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={'type': 'date', 'max': date.today().isoformat()},
                format='%Y-%m-%d'
            ),
            'telefono': forms.TextInput(attrs={'pattern': '[0-9]+', 'title': 'Solo números'}),
        }

class UsuarioUpdateForm(BaseUsuarioForm, forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'fecha_nacimiento']
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={'type': 'date', 'max': date.today().isoformat()},
                format='%Y-%m-%d'
            ),
            'telefono': forms.TextInput(attrs={'pattern': '[0-9]+', 'title': 'Solo números'}),
            'email': forms.EmailInput(attrs={'pattern': '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'}),
        }

class UsuarioContrasenaForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña actual",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña actual',
            'autocomplete': 'current-password'
        }),
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva contraseña',
            'autocomplete': 'new-password'
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña',
            'autocomplete': 'new-password'
        }),
    )

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']