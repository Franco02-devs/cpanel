from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, default='user')

class Trabajador(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    empleado_id = models.CharField(max_length=20, unique=True)
    empleado_nombre = models.CharField(max_length=30, unique=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    rol = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.empleado_nombre}"
