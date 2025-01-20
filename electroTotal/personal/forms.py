from django import forms
from .models import CustomUser, Trabajador, Asistencia

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
        fields = ['empleado_nombre', 'rol_preferido', 'password1','password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['empleado_nombre'].label = 'Nombre del colaborador'
        self.fields['rol_preferido'].label = 'Lugar mas frecuente'
   
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
    def clean_empleado_nombre(self):
        empleado_nombre = self.cleaned_data.get('empleado_nombre')
        if Trabajador.objects.filter(empleado_nombre=empleado_nombre).exists():
            raise forms.ValidationError("Ya existe un colaborador con este nombre")
        return empleado_nombre
    
class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['trabajador','tipo', 'fecha_diferida','lugar',  'lugar_campo', 'foto']
        widgets = {
            'fecha_diferida': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'lugar_campo': forms.TextInput(attrs={'placeholder': 'Especifique el lugar en campo'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['tipo'].initial = 'entrada'
        self.fields['trabajador'].label = 'Colaborador'
        self.fields['tipo'].label = 'Tipo de Asistencia'
        self.fields['fecha_diferida'].label = 'Fecha y Hora de Asistencia (Si es a destiempo)'
        self.fields['lugar'].label = 'Lugar de Registro'
        self.fields['lugar_campo'].label = 'Lugar en Campo (Solo en campo)'
        self.fields['foto'].label = 'Foto (Fecha y Hora)'
        
        # Preseleccionar lugar según el rol preferido
        if user and hasattr(user, 'trabajador'):
            rol_preferido = user.trabajador.rol_preferido
            trabajador=user.trabajador
            self.fields['lugar'].initial = rol_preferido
            self.fields['trabajador'].initial = trabajador
            self.fields['trabajador'].disabled = True
        
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        lugar = cleaned_data.get('lugar')
        
        if 'destiempo' in tipo and not cleaned_data.get('fecha_diferida'):
            self.add_error('fecha_diferida', "La fecha diferida es obligatoria para registros a destiempo.")
        if lugar == 'campo' and not cleaned_data.get('lugar_campo'):
            self.add_error('lugar_campo', "Debe especificar un lugar si el registro es en campo.")
        return cleaned_data
    
   