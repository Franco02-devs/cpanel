from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

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
            return redirect('create_user.html')  # Redirige a una página de éxito o lista de usuarios
    else:
        form = CustomUserCreationForm()

    return render(request, 'create_user.html', {'form': form})
