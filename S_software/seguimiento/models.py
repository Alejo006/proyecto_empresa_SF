from django.db import models

class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True)  # Nombre de usuario
    contrasena = models.CharField(max_length=128)  # Contraseña (usa hashing en el sistema)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    correo = models.EmailField(unique=True)
    cargo = models.CharField(max_length=50, default='administrador') 



class Usuario(models.Model):
    nombreCompleto = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=128, default='123')  # Recuerda: deberías luego cifrarla
    ano_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    documento = models.CharField(max_length=20, unique=True)
    direccion = models.TextField(null=True, blank=True)
    


    def __str__(self):
        return self.nombreCompleto

class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    usuario_asignado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_asignadas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=[
        ('Pendiente', 'Pendiente'),
        ('En progreso', 'En progreso'),
        ('Completada', 'Completada')
    ], default='Pendiente')
    avance = models.TextField(default='Sin avance') 

    def __str__(self):
        return self.nombre
# Create your models here.
