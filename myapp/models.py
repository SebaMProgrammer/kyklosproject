from django.db import models
from django.contrib.auth.models import User


class Empleado(models.Model):
    HORARIO_CHOICES = [
        ('M', 'Mañana'),
        ('T', 'Tarde'),
        ('C', 'Completo'),
        ('O', 'Otros'),
    ]
    ACTIVO_CHOICES = [
        (True, 'SI'),
        (False, 'NO'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    activo = models.BooleanField(choices=ACTIVO_CHOICES, default=True)
    horario = models.CharField(max_length=1, choices=HORARIO_CHOICES, default='O')
    observaciones = models.TextField(blank=True)

    imagen = models.ImageField(upload_to='empleados/', blank=True, null=True, default='default.jpg')  # Default image

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Tarea(models.Model):
    CAMPAÑA_CHOICES = [
        ('BSL', 'BSL'),
        ('JUGUETES', 'Juguetes'),
        ('VIVAMOS', 'Vivamos Circular'),
        ('NINGUNO', 'Ninguno'),
    ]

    nombre = models.CharField(max_length=100)
    campaña = models.CharField(max_length=8, choices=CAMPAÑA_CHOICES, default='NINGUNO')

    def __str__(self):
        return self.nombre

class PuestosDelDia(models.Model):
    HORARIO_CHOICES = [
        ('M', 'Mañana'),
        ('T', 'Tarde'),
        ('C', 'Completo'),
    ]

    fecha = models.DateField()
    horario = models.CharField(max_length=1, choices=HORARIO_CHOICES)

    mesa_1_empleados = models.ManyToManyField(Empleado, related_name='mesa_1', blank=True)
    mesa_1_tareas = models.ManyToManyField(Tarea, related_name='mesa_1_tareas', blank=True)

    mesa_2_empleados = models.ManyToManyField(Empleado, related_name='mesa_2', blank=True)
    mesa_2_tareas = models.ManyToManyField(Tarea, related_name='mesa_2_tareas', blank=True)

    mesa_3_empleados = models.ManyToManyField(Empleado, related_name='mesa_3', blank=True)
    mesa_3_tareas = models.ManyToManyField(Tarea, related_name='mesa_3_tareas', blank=True)

    mesa_4_empleados = models.ManyToManyField(Empleado, related_name='mesa_4', blank=True)
    mesa_4_tareas = models.ManyToManyField(Tarea, related_name='mesa_4_tareas', blank=True)
    
    comentario = models.TextField(blank=True, null=True)

    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Puestos del día {self.fecha}"
    
    class Meta:
        unique_together = ('fecha', 'horario')  # Esta combinación debe ser única