from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg

class Universidad(models.Model):
    nombre = models.CharField(max_length=255)
    pais = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    imagen = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.nombre

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, related_name="usuarios", null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Facultad(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, related_name="facultades")
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.universidad.nombre}"
    
class Profesor(models.Model):
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name="profesores")
    nombre = models.CharField(max_length=255)

    class Meta:
        unique_together = ("facultad", "nombre")

    @property
    def promedio_calificacion(self):
        promedio = self.opiniones.aggregate(promedio=Avg('calificacion'))['promedio']
        return promedio or 0

    def __str__(self):
        return f"{self.nombre} ({self.facultad.nombre})"

class Opinion(models.Model):
    rango_calificacion = [(i, str(i)) for i in range(1,6)]
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="opiniones")
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name="opiniones")
    calificacion = models.IntegerField(choices=rango_calificacion)
    comentario = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.usuario.username} {self.profesor.nombre} ({self.calificacion}/5)"