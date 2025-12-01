from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CuentaPresupuestaria, ActividadProyecto


admin.site.site_header = "Administración I. Municipalidad de Puyehue"
admin.site.site_title = "Portal Gestión Interna"
admin.site.index_title = "Panel de Control DAF / Administración"

@admin.register(CuentaPresupuestaria)
class CuentaAdmin(admin.ModelAdmin):
    # En la lista, mostramos el resultado final. list_editable fue eliminado porque
    # la edición compleja debe hacerse en el formulario de detalle.
    list_display = ('codigo_cuenta', 'nombre_cuenta', 'presupuesto_vigente') 
    search_fields = ('nombre_cuenta', 'codigo_cuenta')

    # Campo de edición detallada: Agrupamos los 3 campos solicitados por DAF.
    fieldsets = (
        (None, {
            'fields': ('codigo_cuenta', 'nombre_cuenta'),
        }),
        ('CONTROL PRESUPUESTARIO (Solo DAF)', {
            # Los campos que DAF puede modificar
            'fields': ('presupuesto_inicial', 'modificaciones', 'presupuesto_vigente'), 
            'classes': ('wide', 'extrapretty'),
            'description': 'Aquí se ingresan las cifras base y las modificaciones, resultando en el Presupuesto Vigente.'
        }),
    )

    # SEGURIDAD: Solo usuarios del grupo "Finanzas_DAF" o Superusuarios pueden editar esto
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser: return True
        return request.user.groups.filter(name='Finanzas_DAF').exists()

    def has_add_permission(self, request):
        if request.user.is_superuser: return True
        return request.user.groups.filter(name='Finanzas_DAF').exists()

@admin.register(ActividadProyecto)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('activity_id', 'nombre_actividad', 'estado_coloreado', 'responsable', 'fecha_termino')
    list_filter = ('estado', 'responsable', 'fecha_termino')
    search_fields = ('nombre_actividad', 'project_id')
    
    # Colores para el estado
    def estado_coloreado(self, obj):
        from django.utils.html import format_html
        colors = {'Completado': 'green', 'En Progreso': 'blue', 'Atrasado': 'red', 'Pendiente': 'orange'}
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', colors.get(obj.estado, 'black'), obj.estado)
    estado_coloreado.short_description = 'Estado'

    def has_change_permission(self, request, obj=None):
        # Si es DAF, retorna Falso (Solo lectura)
        if request.user.groups.filter(name='Finanzas_DAF').exists():
            return False
        return True 

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='Finanzas_DAF').exists():
            return False
        return True

    def has_add_permission(self, request):
        if request.user.groups.filter(name='Finanzas_DAF').exists():
            return False
        return True