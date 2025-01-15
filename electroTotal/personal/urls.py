from django.urls import path
from . import views

urlpatterns = [
    path('create_user/', views.create_user_view, name='create_user'),
    path('create_trabajador/', views.create_trabajador_view, name='create_trabajador'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
