from django.urls import path
from . import views

urlpatterns = [
    path('create_user/', views.create_user_view, name='create_user'),
    path('create_trabajador/', views.create_trabajador_view, name='create_trabajador'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('home2',views.home_view2, name='home2'),
    path('trabajador_creado/<int:trabajador_id>/', views.trabajador_creado_view, name='trabajador_creado'),
    path('user_creado/<int:user_id>/', views.user_created_view, name='user_creado'),
    path('admin/dashboard/', views.dashboard_view, name='admin_dashboard'),
    path('registrar_asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('confirmacion/<int:asistencia_id>/', views.confirmacion_asistencia, name='confirmacion_asistencia'),
    path('list/', views.asistencia_completa_view, name='asistencia_completa'),
    path('trabajadores/', views.lista_trabajadores, name='lista_trabajadores'),
    path('trabajadores/<int:trabajador_id>/asistencias/', views.asistencias_trabajador, name='asistencias_trabajador'),
    path('asistencia/detalle/<int:id>/', views.asistencia_detalle, name='asistencia_detalle'),
    path('excel/', views.generar_excel_asistencias, name='excel'),
]
