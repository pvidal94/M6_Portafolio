from django.db import models
from django.contrib.auth.models import User

class CuentaPresupuestaria(models.Model):
    codigo_cuenta = models.CharField(max_length=50, unique=True, verbose_name="Código Presupuestario")
    nombre_cuenta = models.CharField(max_length=200, verbose_name="Nombre de la Cuenta")
    
    # CAMPOS SOLICITADOS PARA EDICIÓN POR DAF
    presupuesto_inicial = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Presupuesto Inicial")
    modificaciones = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Modificaciones Actuales")
    presupuesto_vigente = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Presupuesto Final Vigente")

    def __str__(self):
        return f"{self.codigo_cuenta} - {self.nombre_cuenta}"

class ActividadProyecto(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En Progreso', 'En Progreso'),
        ('Completado', 'Completado'),
        ('Atrasado', 'Atrasado'),
    ]
    
    OFICINAS = [
        ('SECPLAN', 'Secretaría Comunal de Planificación'),
        ('DIDECO', 'Desarrollo Comunitario'),
        ('DOM', 'Dirección de Obras'),
        ('TRANSITO', 'Dirección de Tránsito'),
        ('ALCALDIA', 'Gabinete Alcaldía'),
    ]

    activity_id = models.CharField(max_length=20, unique=True, verbose_name="ID Actividad")
    project_id = models.CharField(max_length=20, verbose_name="ID Proyecto")
    nombre_actividad = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    # Aquí simulamos la oficina responsable
    responsable = models.CharField(max_length=20, choices=OFICINAS, default='SECPLAN') 
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"[{self.responsable}] {self.nombre_actividad}"