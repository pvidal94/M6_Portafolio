from django import forms
from .models import ActividadProyecto, CuentaPresupuestaria

class ActividadForm(forms.ModelForm):
    class Meta:
        model = ActividadProyecto
        fields = ['activity_id', 'project_id', 'nombre_actividad', 'fecha_inicio', 'fecha_termino', 'estado', 'responsable']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'activity_id': forms.TextInput(attrs={'class': 'form-control'}),
            'project_id': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_actividad': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = CuentaPresupuestaria
        fields = '__all__'
        widgets = {
            'codigo_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'presupuesto_inicial': forms.NumberInput(attrs={'class': 'form-control'}),
            'modificaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'presupuesto_vigente': forms.NumberInput(attrs={'class': 'form-control'}),
            'porcentaje_ejecucion': forms.NumberInput(attrs={'class': 'form-control'}),
        }