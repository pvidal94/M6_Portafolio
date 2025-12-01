from django.contrib import admin
from django.urls import path
from gestion_municipal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticación
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard y Memoria
    path('dashboard/', views.dashboard, name='dashboard'),
    path('memoria-tecnica/', views.memoria_tecnica, name='memoria_tecnica'),
    
    # Actividades
    path('actividades/', views.lista_actividades, name='lista_actividades'),
    path('actividades/nueva/', views.crear_actividad, name='crear_actividad'),
    path('actividades/eliminar/<int:id>/', views.eliminar_actividad, name='eliminar_actividad'),
]