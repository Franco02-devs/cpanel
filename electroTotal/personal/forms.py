from django import forms
from .models import CustomUser, Trabajador

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña", required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña", required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'user_type', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username


    
class TrabajadorCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña", required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña", required=True)

    class Meta:
        model = Trabajador
        fields = ['empleado_nombre', 'departamento', 'rol', 'password1','password2']
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
    def clean_username(self):
        empleado_nombre = self.cleaned_data.get('empleado_nombre')
        if Trabajador.objects.filter(empleado_nombre=empleado_nombre).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return empleado_nombre

