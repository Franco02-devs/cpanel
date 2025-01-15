from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Trabajador

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'user_type']
    
class TrabajadorCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña", required=True)

    class Meta:
        model = Trabajador
        fields = ['empleado_nombre', 'departamento', 'rol', 'password']

