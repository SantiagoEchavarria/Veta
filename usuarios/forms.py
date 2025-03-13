from django import forms
from django.contrib.auth.forms import UserCreationForm,  PasswordChangeForm
from .models import Usuario
from django.contrib.auth import password_validation


class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'fecha_nacimiento', 'password1', 'password2']
        
class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'fecha_nacimiento'] 

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