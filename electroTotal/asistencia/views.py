from django.shortcuts import render, redirect
from .forms import AsistenciaForm
from .models import Asistencia
from django.contrib.auth.decorators import login_required

@login_required
def registrar_asistencia(request):
    trabajador = request.user.trabajador  # Obtener el trabajador del usuario logueado
    
    if request.method == 'POST':
        form = AsistenciaForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            asistencia = form.save(commit=False)
            asistencia.trabajador = trabajador  # Asegurar que se asigna el trabajador logueado
            asistencia.save()
            return redirect('asistencia_list')  # Redirigir a la lista de asistencias u otra vista

    else:
        form = AsistenciaForm(user=request.user)
    
    return render(request, 'registrar_asistencia.html', {'form': form})
