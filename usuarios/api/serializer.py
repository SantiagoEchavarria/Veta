from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from ..models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    # Campo adicional para la contraseña (solo escritura)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]  # Valida la contraseña según AUTH_PASSWORD_VALIDATORS
    )
    
    # Campo calculado para la URL de Gravatar (solo lectura)
    gravatar_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'email',
            'nombre',
            'password',
            'telefono',
            'fecha_nacimiento',
            'primera_vez',
            'gravatar_url',  # Incluye el campo personalizado
        ]
        extra_kwargs = {
            'email': {'required': True},
            'nombre': {'required': True},
        }

    def get_gravatar_url(self, obj):
        # Llama al método del modelo para obtener la URL de Gravatar
        return obj.get_gravatar_url()

    def create(self, validated_data):
        # Crea el usuario con la contraseña hasheada
        password = validated_data.pop('password')
        user = Usuario.objects.create(**validated_data)
        user.set_password(password)  # Hashea la contraseña
        user.save()
        return user