from rest_framework import serializers
from .models import Facultad, Profesor, Universidad, CustomUser, Opinion
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ProfesorSerializer(serializers.ModelSerializer):
    promedio_calificacion = serializers.FloatField(read_only=True)
    class Meta:
        model = Profesor
        fields = ["id", "nombre", "facultad", "promedio_calificacion"]
        extra_kwargs = {
            "facultad" : {"read_only" : True}, 
            "nombre" : {
                "error_messages" : {
                    "unique" : "El profesor ya existe en esta facultad."
                }
            }
        }
    
    def validate(self, data):
        nombre = data.get("nombre")
        facultad = self.context["view"].kwargs["facultad_id"]

        if Profesor.objects.filter(nombre=nombre, facultad=facultad).exists():
            raise serializers.ValidationError({"nombre" : "Este profesor ya existe en esta facultad."})
        return data

class FacultadSerializer(serializers.ModelSerializer):
    profesores = ProfesorSerializer(many=True, read_only=True)
    class Meta:
        model = Facultad
        fields = ["id", "nombre", "profesores"]

class UniversidadSerializer(serializers.ModelSerializer):
    facultades = FacultadSerializer(many=True, read_only=True)
    class Meta:
        model = Universidad
        fields = ["id", "nombre", "pais", "ciudad", "facultades", "imagen"]

class UsuarioSerializer(serializers.ModelSerializer):
    universidad = serializers.PrimaryKeyRelatedField(
        queryset = Universidad.objects.all()
    )
    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "email", "universidad"]
        extra_kwargs = {"password": {"write_only": True},
            "username": {
                "error_messages": {
                    "unique": "El nombre de usuario ya existe."
                }
            },
            "email": {
                "error_messages": {
                    "unique": "El correo ya está en uso."
                }
            }
        }

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError({"username" : "El nombre de usuario ya existe."})
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError({"email" : "El correo ya está en uso."})
        return value
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class OpinionSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    profesor = ProfesorSerializer(read_only=True)
    class Meta:
        model = Opinion
        fields = ["id", "usuario", "profesor", "calificacion", "comentario"]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['universidad'] = user.universidad.id
        return token