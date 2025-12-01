import csv
from datetime import date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from gestion_municipal.models import ActividadProyecto, CuentaPresupuestaria

class Command(BaseCommand):
    help = 'Carga usuarios, roles, permisos y datos base (Presupuesto Global)'
    password_default = 'TheStrokes94.'
    
    def handle(self, *args, **kwargs):
        self.stdout.write("🛠️ Iniciando configuración de la Municipalidad de Puyehue...")

        # --- 1. CONFIGURACIÓN DE MODELOS ---
        
        # Eliminar datos existentes (para evitar duplicados al correr varias veces)
        ActividadProyecto.objects.all().delete()
        CuentaPresupuestaria.objects.all().delete()

        # Obtener ContentTypes (Identificadores de las tablas)
        ct_actividad = ContentType.objects.get_for_model(ActividadProyecto)
        ct_presupuesto = ContentType.objects.get_for_model(CuentaPresupuestaria)

        # --- 2. CREACIÓN DE GRUPOS Y PERMISOS ---

        grupo_admin, _ = Group.objects.get_or_create(name='Administracion_Municipal')
        grupo_daf, _ = Group.objects.get_or_create(name='Finanzas_DAF')
        grupo_lectura, _ = Group.objects.get_or_create(name='Directores_Lectura')

        # Permisos
        permisos_admin = Permission.objects.filter(
            content_type=ct_actividad, 
            codename__in=['add_actividadproyecto', 'change_actividadproyecto', 'delete_actividadproyecto']
        )
        permiso_daf_presupuesto_change = Permission.objects.get(
            content_type=ct_presupuesto, codename='change_cuentapresupuestaria'
        )
        permiso_ver_todo = Permission.objects.filter(codename__startswith='view_') # Permiso genérico de visualización
        
        # Asignación de Permisos
        grupo_admin.permissions.set(permisos_admin)
        grupo_daf.permissions.add(permiso_daf_presupuesto_change)
        grupo_lectura.permissions.set(permiso_ver_todo)

        # --- 3. CREACIÓN DE USUARIOS ---
        
        users_data = [
            {'user': 'administrador_municipal', 'email': 'admin@puyehue.cl', 'group': grupo_admin},
            {'user': 'director_finanzas', 'email': 'daf@puyehue.cl', 'group': grupo_daf},
            {'user': 'dideco', 'email': 'dideco@puyehue.cl', 'group': grupo_lectura},
            {'user': 'director_control', 'email': 'control@puyehue.cl', 'group': grupo_lectura},
            {'user': 'alcalde', 'email': 'alcalde@puyehue.cl', 'group': grupo_lectura},
        ]

        for u in users_data:
            user, created = User.objects.get_or_create(username=u['user'], email=u['email'])
            user.set_password(self.password_default)
            user.is_staff = True
            user.save()
            user.groups.set([u['group']])
            self.stdout.write(f"👤 Usuario {u['user']} ({u['group'].name}) -> Creado/Actualizado")

        # --- 4. CARGA DE PRESUPUESTO  ---
        
        CuentaPresupuestaria.objects.create(
            codigo_cuenta='000000',
            nombre_cuenta='PRESUPUESTO GENERAL ANUAL',
            presupuesto_inicial=Decimal('2500000000'),
            modificaciones=Decimal('-150000000'),
            presupuesto_vigente=Decimal('2350000000') # El valor que sumará el Dashboard
        )
        self.stdout.write(self.style.SUCCESS("💰 Cuenta de Presupuesto Global CREADA."))


        # --- 5. CARGA DE ACTIVIDADES   ---
        
        actividades = [
            {"id": "ACT-001", "proy": "PR-2025-INFRA", "nombre": "Mejoramiento Costanera Entre Lagos", "inicio": date(2025, 1, 15), "fin": date(2025, 6, 30), "estado": "En Progreso", "resp": "DOM"},
            {"id": "ACT-002", "proy": "PR-2025-SOCIAL", "nombre": "Operativo Veterinario Rural Pilmaiquén", "inicio": date(2025, 2, 1), "fin": date(2025, 2, 5), "estado": "Pendiente", "resp": "DIDECO"},
            {"id": "ACT-003", "proy": "PR-2024-URB", "nombre": "Recambio Luminarias Villa Los Lagos", "inicio": date(2024, 11, 1), "fin": date(2024, 12, 15), "estado": "Completado", "resp": "SECPLAN"},
        ]

        for item in actividades:
            ActividadProyecto.objects.get_or_create(
                activity_id=item["id"],
                defaults={
                    # Mapeo: Nombre del campo del modelo = Valor del diccionario
                    "project_id": item["proy"],
                    "nombre_actividad": item["nombre"],
                    "fecha_inicio": item["inicio"],
                    "fecha_termino": item["fin"],
                    "estado": item["estado"],
                    "responsable": item["resp"],
                }
            )
        self.stdout.write(self.style.SUCCESS(f"✅ Carga completa. {len(actividades)} actividades cargadas."))