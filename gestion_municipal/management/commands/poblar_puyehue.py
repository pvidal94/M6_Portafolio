from django.core.management.base import BaseCommand
from gestion_municipal.models import ActividadProyecto
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Carga datos iniciales de la I. Municipalidad de Puyehue'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando carga de datos municipales...")

        actividades = [
            {
                "id": "ACT-001", "proy": "PR-2024-TUR", 
                "nombre": "Mejoramiento Costanera Entre Lagos", 
                "inicio": date(2025, 1, 15), "fin": date(2025, 6, 30), 
                "estado": "En Progreso", "resp": "DOM"
            },
            {
                "id": "ACT-002", "proy": "PR-2024-SOC", 
                "nombre": "Operativo Veterinario Rural (Pilmaiquén)", 
                "inicio": date(2025, 2, 1), "fin": date(2025, 2, 5), 
                "estado": "Pendiente", "resp": "DIDECO"
            },
            {
                "id": "ACT-003", "proy": "PR-2024-VIL", 
                "nombre": "Recambio Luminarias Villa Los Lagos", 
                "inicio": date(2024, 11, 1), "fin": date(2024, 12, 15), 
                "estado": "Completado", "resp": "SECPLAN"
            },
            {
                "id": "ACT-004", "proy": "PR-2024-EDU", 
                "nombre": "Mantención Calefacción Escuelas Municipales", 
                "inicio": date(2025, 3, 1), "fin": date(2025, 3, 15), 
                "estado": "Atrasado", "resp": "DOM"
            },
            {
                "id": "ACT-005", "proy": "PR-2024-TRA", 
                "nombre": "Señalética Ruta 215 (Cruce Termas)", 
                "inicio": date(2025, 4, 10), "fin": date(2025, 4, 20), 
                "estado": "Pendiente", "resp": "TRANSITO"
            },
        ]

        for item in actividades:
            obj, created = ActividadProyecto.objects.get_or_create(
                activity_id=item["id"],
                defaults={
                    "project_id": item["proy"],
                    "nombre_actividad": item["nombre"],
                    "fecha_inicio": item["inicio"],
                    "fecha_termino": item["fin"],
                    "estado": item["estado"],
                    "responsable": item["resp"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Creada: {item["nombre"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Ya existe: {item["nombre"]}'))

        self.stdout.write(self.style.SUCCESS('✅ ¡Datos de Puyehue cargados exitosamente!'))