from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, TrabajadorCreationForm
from .models import CustomUser, Trabajador
from .scripts import getFirstWord, generate_unique_username
from django.contrib.auth.forms import AuthenticationForm


# Vista de creación de usuario solo accesible para superadmins
@user_passes_test(lambda u: u.is_superuser)
def create_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Crear un nuevo usuario
            user = form.save(commit=False)  # No guardar aún para aplicar la contraseña
            user.set_password(form.cleaned_data['password1'])  # Usar set_password para hash de la contraseña
            user.save()  # Guardar el usuario con la contraseña ya segura
            return redirect('home')  # Redirige a una página de éxito o lista de usuarios
    else:
        form = CustomUserCreationForm()

    return render(request, 'create_user.html', {'form': form})

# Vista para crear un trabajador solo accesible para superadmins
@user_passes_test(lambda u: u.is_superuser)
def create_trabajador_view(request):
    if request.method == 'POST':
        form = TrabajadorCreationForm(request.POST)
        if form.is_valid():
            trabajador = form.save(commit=False)
            # Obtener la contraseña ingresada por el admin
            password = form.cleaned_data['password1']
            # Crear el usuario asociado al trabajador
            username=generate_unique_username(trabajador.empleado_nombre)
            user = CustomUser.objects.create_user(
                username=username,
                password=password  # Usar la contraseña proporcionada por el admin
            )
            # Asocia el trabajador al usuario
            user.username=username+str(user.id)+str(int(user.is_staff))
            user.save()
            trabajador.user = user
            trabajador.empleado_id=str(user.id)
            # Guarda el trabajador (ahora con el usuario asociado)
            trabajador.save()
            messages.success(request, "Trabajador creado exitosamente.")
            return redirect('trabajador_creado', trabajador_id=trabajador.id)
    else:
        form = TrabajadorCreationForm()

    return render(request, 'create_trabajador.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Autenticar al usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirigir al home o la página principal
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige a la página de login o donde desees

@user_passes_test(lambda u: u.is_superuser)
def trabajador_creado_view(request, trabajador_id):
    trabajador = Trabajador.objects.get(id=trabajador_id)
    
    # Pasamos los detalles del trabajador a la plantilla
    return render(request, 'trabajador_creado.html', {'trabajador': trabajador})



# Vista de Home
def home_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        mensaje = f"Hola {username}!"
    else:
        mensaje = "¡Inicia sesión!"
    
    return render(request, 'home.html', {'mensaje': mensaje})


