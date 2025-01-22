from django import forms
from .models import CustomUser, Trabajador, Asistencia
from .scripts import getFirstWord

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña", required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña", required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'user_type', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['user_type'].label = 'Tipo de usuario(user/admin):'
        self.fields['first_name'].label = 'Nombre del colaborador:'


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
    
    def clean_empleado_nombre(self):
        empleado_nombre = self.cleaned_data.get('empleado_nombre')
        if Trabajador.objects.filter(empleado_nombre=empleado_nombre).exists():
            raise forms.ValidationError("Ya existe un colaborador con este nombre")
        return empleado_nombre

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
    
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['trabajador', 'tipo', 'fecha_diferida', 'lugar', 'lugar_campo', 'foto']
        widgets = {
            'fecha_diferida': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'lugar_campo': forms.TextInput(attrs={'placeholder': 'Especifique el lugar en campo'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['tipo'].initial = 'entrada'
        self.fields['trabajador'].label = 'Colaborador'
        self.fields['tipo'].label = 'Tipo de Asistencia'
        self.fields['fecha_diferida'].label = 'Fecha y Hora de Asistencia (Si es a destiempo)'
        self.fields['lugar'].label = 'Lugar de Registro'
        self.fields['lugar_campo'].label = 'Lugar en Campo (Solo en campo)'
        self.fields['foto'].label = 'Foto (Fecha y Hora)'
        
        if self.user and hasattr(self.user, 'trabajador'):
            self.fields['lugar'].initial = self.user.trabajador.rol_preferido
            self.fields['trabajador'].initial = self.user.trabajador
            self.fields['trabajador'].disabled = True
            if self.user.user_type=='admin':
                self.fields['trabajador'].disabled = False
            ultimo_registro = Asistencia.objects.filter(trabajador=self.user.trabajador).order_by('-id').first()
            if ultimo_registro:
                if getFirstWord(str(ultimo_registro.tipo))=='entrada':
                    self.fields['tipo'].initial = 'salida'
                else:
                    self.fields['tipo'].initial = 'entrada'                  
                    

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        fecha_diferida = cleaned_data.get('fecha_diferida')
        lugar = cleaned_data.get('lugar')
        lugar_campo = cleaned_data.get('lugar_campo')

        # Validación de tipo y fecha diferida
        if 'destiempo' in tipo and not fecha_diferida:
            self.add_error('fecha_diferida', _("La fecha diferida es obligatoria para registros a destiempo."))
        if lugar == 'campo' and not lugar_campo:
            self.add_error('lugar_campo', _("Debe especificar un lugar si el registro es en campo."))

        # Validación de entrada/salida consecutivas
        self.validar_registro_consecutivo(cleaned_data)
        return cleaned_data

    def validar_registro_consecutivo(self, cleaned_data):
        tipo = cleaned_data.get('tipo')
        trabajador = cleaned_data.get('trabajador')
        if trabajador:
            ultimo_registro = Asistencia.objects.filter(trabajador=trabajador).order_by('-id').first()
            if ultimo_registro:
                tipo_actual = tipo.split()[0]  # Suponiendo que el tipo tiene prefijos como 'entrada' o 'salida'
                tipo_ultimo = ultimo_registro.tipo.split()[0]
                if tipo_actual == tipo_ultimo:
                    raise ValidationError(
                        _("No se puede registrar dos veces seguidas el mismo tipo de asistencia. Último registro: %(fecha)s - %(tipo)s"),
                        code='invalid',
                        params={'fecha': ultimo_registro.fecha.strftime("%d-%m-%Y %H:%M:%S"), 'tipo': ultimo_registro.tipo.upper()}
                    )
            elif tipo in ['salida', 'salida a destiempo']:
                raise ValidationError(_("No puedes registrar una salida sin haber registrado previamente tu entrada."))


    
   