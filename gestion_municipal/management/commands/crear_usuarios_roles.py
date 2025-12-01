from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from gestion_municipal.models import ActividadProyecto, CuentaPresupuestaria

class Command(BaseCommand):
    help = 'Crea usuarios y asigna permisos jerárquicos para Muni Puyehue'

    def handle(self, *args, **kwargs):
        self.stdout.write("🔐 Configurando Seguridad y Roles...")

        # 1. Definir Grupos
        grupo_admin, _ = Group.objects.get_or_create(name='Administracion_Municipal')
        grupo_daf, _ = Group.objects.get_or_create(name='Finanzas_DAF')
        grupo_lectura, _ = Group.objects.get_or_create(name='Directores_Lectura')

        # 2. Obtener ContentTypes (Identificadores de las tablas)
        ct_actividad = ContentType.objects.get_for_model(ActividadProyecto)
        ct_presupuesto = ContentType.objects.get_for_model(CuentaPresupuestaria)

        # 3. Asignar Permisos a los Grupos
        
        # --- PERMISOS ADMIN MUNICIPAL (Actividades: Full Control) ---
        permisos_admin = Permission.objects.filter(
            content_type=ct_actividad, 
            codename__in=['add_actividadproyecto', 'change_actividadproyecto', 'delete_actividadproyecto']
        )
        grupo_admin.permissions.set(permisos_admin)

        # --- PERMISOS DAF (Presupuesto: Modificar / Actividades: Ver) ---
        permiso_daf_presupuesto = Permission.objects.get(
            content_type=ct_presupuesto, codename='change_cuentapresupuestaria'
        )
        permiso_ver_actividades = Permission.objects.get(
            content_type=ct_actividad, codename='view_actividadproyecto'
        )
        grupo_daf.permissions.add(permiso_daf_presupuesto, permiso_ver_actividades)

        # --- PERMISOS LECTURA (Solo Ver) ---
        grupo_lectura.permissions.add(permiso_ver_actividades)

        # 4. Crear Usuarios y Asignar Roles
        users_data = [
            {'user': 'administrador_municipal', 'email': 'admin@puyehue.cl', 'group': grupo_admin},
            {'user': 'director_finanzas', 'email': 'daf@puyehue.cl', 'group': grupo_daf},
            {'user': 'dideco', 'email': 'dideco@puyehue.cl', 'group': grupo_lectura},
            {'user': 'director_control', 'email': 'control@puyehue.cl', 'group': grupo_lectura},
            {'user': 'alcalde', 'email': 'alcalde@puyehue.cl', 'group': grupo_lectura},
        ]

        for u in users_data:
            user, created = User.objects.get_or_create(username=u['user'], email=u['email'])
            user.set_password('TheStrokes94.') # Contraseña solicitada
            user.is_staff = True # Permitir acceso al Admin Panel para gestionar sus áreas
            user.save()
            user.groups.clear()
            user.groups.add(u['group'])
            
            action = "Creado" if created else "Actualizado"
            self.stdout.write(f"👤 Usuario {u['user']} ({u['group'].name}) -> {action}")

        self.stdout.write(self.style.SUCCESS("✅ ¡Usuarios y Permisos configurados correctamente!"))