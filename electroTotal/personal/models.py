from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=10, default='user',choices=[('user', 'User'), ('admin', 'Admin')])

class Trabajador(models.Model):
    ultimaAsistenciaProcesada=1
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    empleado_id = models.CharField(max_length=20, unique=True)
    empleado_nombre = models.CharField(max_length=30, unique=True)
    rol_preferido = models.CharField(max_length=50, choices=[('campo', 'Campo'), ('oficina', 'Oficina')], default='campo',null=True,blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.empleado_nombre}"
class Asistencia(models.Model):
    
    def obtener_hora_actual():
        return timezone.now().time()
    
    elegirLugar=[('oficina', 'Oficina'),
        ('campo', 'Campo'),]
    elegirTipoRegistro=[('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('entrada a destiempo', 'Entrada a destiempo'),
        ('salida a destiempo', 'Salida a destiempo')]
    
    trabajador=models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    lugar=models.CharField(max_length=10,choices=elegirLugar)
    lugar_campo=models.CharField(max_length=100,blank=True,null=True)
    tipo=models.CharField(max_length=20,choices=elegirTipoRegistro)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=obtener_hora_actual)
    fecha_diferida = models.DateTimeField(null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_asistencia/')
    finalFecha=models.DateField(default=timezone.now)
    finalHora=models.TimeField(default=obtener_hora_actual)

    def __str__(self):
        warn=""
        if self.fecha_diferida:
            warn="DIFF! "
        return f"{warn}{self.trabajador.empleado_nombre} - {self.tipo} - {self.fecha} {self.hora}"
    
class AsistenciaCompleta(models.Model):
         
    trabajador=models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    entrada=models.ForeignKey(Asistencia, on_delete=models.CASCADE, related_name='entrada_completa')
    salida=models.ForeignKey(Asistencia, on_delete=models.CASCADE, related_name='salida_completa')
    
    def __str__(self):
        final=""
        if self.salida:
            final=str(self.salida.hora.strftime("%H:%M:%S"))
        return f"{str(self.entrada.hora.strftime("%H:%M:%S"))} - {final}"