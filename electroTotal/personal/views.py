from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, TrabajadorCreationForm, AsistenciaForm
from .models import CustomUser, Trabajador, Asistencia
from .scripts import generate_unique_username, getFirstWord
from django.contrib.auth.forms import AuthenticationForm

@user_passes_test(lambda u: u.is_superuser)
def create_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            trabajador=Trabajador.objects.create(
                user=user,
                empleado_id=str(user.id),
                empleado_nombre=form.cleaned_data['first_name'],          
            )
            return redirect('user_creado', user_id=user.id)
    else:
        form = CustomUserCreationForm()

    return render(request, 'create_user.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser or (u.user_type=="admin"))
def create_trabajador_view(request):
    if request.method == 'POST':
        form = TrabajadorCreationForm(request.POST)
        if form.is_valid():
            trabajador = form.save(commit=False)
            password = form.cleaned_data['password1']
            username=generate_unique_username(trabajador.empleado_nombre)
            user = CustomUser.objects.create_user(
                username=username,
                password=password
            )
            user.username=username+str(user.id)+str(int(user.is_staff))
            user.save()
            trabajador.user = user
            trabajador.empleado_id=str(user.id)
            trabajador.save()
            messages.success(request, "Trabajador creado exitosamente.")
            return redirect('trabajador_creado', trabajador_id=trabajador.id)
    else:
        form = TrabajadorCreationForm()

    return render(request, 'create_trabajador.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser or (u.user_type=="admin"))
def trabajador_creado_view(request, trabajador_id):
    trabajador = Trabajador.objects.get(id=trabajador_id)
    return render(request, 'trabajador_creado.html', {'trabajador': trabajador})

@user_passes_test(lambda u: u.is_superuser)
def user_created_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'user_creado.html', {'user': user})

@user_passes_test(lambda u: u.is_superuser or (u.user_type=="admin"))
def dashboard_view(request):
    return render(request, 'admin_dashboard.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type=="admin" or user.is_superuser :
                    return redirect('home2')
                else:
                    return redirect("home")
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        mensaje = f"Hola {username}!"
    else:
        mensaje = "¡Inicia sesión!"
    
    return render(request, 'home.html', {'mensaje': mensaje})
    
@user_passes_test(lambda u: u.is_superuser or (u.user_type=="admin"))
def home_view2(request):
    if request.user.is_authenticated:
        username = request.user.username
        mensaje = f"Hola {username}!"
    else:
        mensaje = "¡Inicia sesión!"
    
    return render(request, 'home2.html', {'mensaje': mensaje})

@login_required
def registrar_asistencia(request):
    trabajador = request.user.trabajador  # Obtener el trabajador del usuario logueado
    
    if request.method == 'POST':
        form = AsistenciaForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            asistencia = form.save(commit=False)
            # Si hay un último registro
            ultimo_registro = Asistencia.objects.filter(trabajador=asistencia.trabajador,).order_by('-id').first()
            # Obtenemos el último registro, si existe
            
            if ultimo_registro:
                controlUltimoRegistro=getFirstWord(ultimo_registro.tipo)
                controlAsistenciaTipo=getFirstWord(asistencia.tipo)
                if controlUltimoRegistro==controlAsistenciaTipo:
                    error="Si aún no has registrado tu salida no puedes marcar una nueva entrada. Tampoco marcar 2 salidas seguidas, ÚLTIMO REGISTRO:   "+str(ultimo_registro.fecha.strftime("%d-%m-%Y %H:%M:%S"))+" "+((ultimo_registro.tipo).upper())
                    messages.error(request,error)
                    return redirect('registrar_asistencia')
                # Si no hay un último registro, significa que es el primer registro del día
            elif (asistencia.tipo == 'salida')| (asistencia.tipo == 'salida a destiempo'):
                messages.error(request, 'No puedes registrar una salida sin haber registrado previamente tu entrada.')
                return redirect('registrar_asistencia')
            asistencia.trabajador = trabajador  # Asegurar que se asigna el trabajador logueado
            asistencia.save()
            return redirect('home')  # Redirigir a la lista de asistencias u otra vista
    else:
        form = AsistenciaForm(user=request.user)
    
    return render(request, 'registrar_asistencia.html', {'form': form})


