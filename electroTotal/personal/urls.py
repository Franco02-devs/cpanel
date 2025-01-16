from django.urls import path
from . import views

urlpatterns = [
    path('create_user/', views.create_user_view, name='create_user'),
    path('create_trabajador/', views.create_trabajador_view, name='create_trabajador'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('trabajador_creado/<int:trabajador_id>/', views.trabajador_creado_view, name='trabajador_creado'),

]
